"""Integración con Claude API para generar respuestas."""

import anthropic
from voice_agent.config import cfg, ANTHROPIC_API_KEY
from voice_agent.rag import DocumentStore


class ClaudeAgent:
    def __init__(self, doc_store: DocumentStore):
        if not ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY no configurada en .env")
        self._client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        self._doc_store = doc_store
        self._model = cfg["claude"]["model"]
        self._max_tokens = cfg["claude"]["max_tokens"]
        self._system_base = cfg["claude"]["system_prompt"]
        self._history: list[dict] = []

    def answer(self, question: str) -> str:
        """Busca contexto en documentos y genera respuesta con Claude."""
        context_chunks = self._doc_store.search(question)

        system = self._system_base
        if context_chunks:
            context_text = "\n\n---\n\n".join(context_chunks)
            system += f"\n\n# Contexto de tus documentos:\n{context_text}"
        else:
            system += "\n\n# Nota: No encontré información relevante en los documentos."

        self._history.append({"role": "user", "content": question})

        response = self._client.messages.create(
            model=self._model,
            max_tokens=self._max_tokens,
            system=system,
            messages=self._history,
        )

        answer_text = response.content[0].text.strip()
        self._history.append({"role": "assistant", "content": answer_text})

        # Mantiene historial máximo de 10 turnos para no exceder context window
        if len(self._history) > 20:
            self._history = self._history[-20:]

        return answer_text

    def reset_history(self):
        """Reinicia el historial de conversación (nueva reunión)."""
        self._history = []
