"""RAG: carga documentos y busca contexto relevante con ChromaDB."""

from pathlib import Path
from typing import Optional
from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
    UnstructuredExcelLoader,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_anthropic import AnthropicEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from voice_agent.config import cfg, DOCUMENTS_DIR, CHROMA_DIR, ANTHROPIC_API_KEY


_SUPPORTED = {
    ".pdf": PyPDFLoader,
    ".docx": Docx2txtLoader,
    ".txt": TextLoader,
    ".md": TextLoader,
    ".xlsx": UnstructuredExcelLoader,
    ".csv": TextLoader,
}


def _get_embeddings():
    # Usa embeddings locales (sin costo) — HuggingFace sentence-transformers
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        model_kwargs={"device": "cpu"},
    )


class DocumentStore:
    def __init__(self):
        self._embeddings = _get_embeddings()
        self._db: Optional[Chroma] = None
        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=cfg["rag"]["chunk_size"],
            chunk_overlap=cfg["rag"]["chunk_overlap"],
        )
        # Carga la base existente si existe
        if CHROMA_DIR.exists():
            self._db = Chroma(
                persist_directory=str(CHROMA_DIR),
                embedding_function=self._embeddings,
            )

    def ingest(self, path: Optional[Path] = None) -> int:
        """Indexa todos los documentos del directorio (o un archivo específico)."""
        docs_to_load = []

        if path and path.is_file():
            sources = [path]
        else:
            sources = list(DOCUMENTS_DIR.rglob("*"))

        for src in sources:
            if src.suffix.lower() not in _SUPPORTED:
                continue
            loader_cls = _SUPPORTED[src.suffix.lower()]
            try:
                loader = loader_cls(str(src))
                docs_to_load.extend(loader.load())
            except Exception as e:
                print(f"  [!] No se pudo cargar {src.name}: {e}")

        if not docs_to_load:
            return 0

        chunks = self._splitter.split_documents(docs_to_load)

        self._db = Chroma.from_documents(
            documents=chunks,
            embedding=self._embeddings,
            persist_directory=str(CHROMA_DIR),
        )
        return len(chunks)

    def search(self, query: str, k: Optional[int] = None) -> list[str]:
        """Devuelve los fragmentos más relevantes para la consulta."""
        if self._db is None:
            return []
        k = k or cfg["rag"]["top_k"]
        results = self._db.similarity_search(query, k=k)
        return [doc.page_content for doc in results]

    @property
    def has_documents(self) -> bool:
        return self._db is not None

    def list_sources(self) -> list[str]:
        if self._db is None:
            return []
        try:
            data = self._db.get(include=["metadatas"])
            sources = {m.get("source", "desconocido") for m in data["metadatas"]}
            return sorted(sources)
        except Exception:
            return []
