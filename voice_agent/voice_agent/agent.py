"""Orquestador principal del agente de voz."""

from rich.console import Console
from rich.panel import Panel
from rich.status import Status
from voice_agent.stt import SpeechToText
from voice_agent.tts import TextToSpeech
from voice_agent.rag import DocumentStore
from voice_agent.claude_agent import ClaudeAgent
from voice_agent.config import cfg

console = Console()


class VoiceAgent:
    def __init__(self):
        console.print(Panel.fit(
            "[bold cyan]Agente de Voz para Zoom[/bold cyan]\n"
            "Powered by Claude + ElevenLabs + Whisper",
            border_style="cyan"
        ))

        with Status("[yellow]Cargando modelos...[/yellow]"):
            self.doc_store = DocumentStore()
            self.stt = SpeechToText()
            self.tts = TextToSpeech()
            self.claude = ClaudeAgent(self.doc_store)

        if self.doc_store.has_documents:
            sources = self.doc_store.list_sources()
            console.print(f"[green]✓[/green] {len(sources)} documento(s) indexado(s)")
        else:
            console.print("[yellow]⚠[/yellow] Sin documentos indexados. Agrega archivos a ./documents/ y ejecuta: python main.py ingest")

    def run_once(self) -> tuple[str, str] | tuple[None, None]:
        """Un ciclo: escucha → transcribe → responde → habla."""
        console.print("\n[dim]Escuchando...[/dim] (habla cuando quieras)")

        text = self.stt.listen()
        if not text:
            return None, None

        console.print(f"[bold white]Pregunta:[/bold white] {text}")

        with Status("[cyan]Consultando Claude...[/cyan]"):
            answer = self.claude.answer(text)

        console.print(f"[bold green]Respuesta:[/bold green] {answer}")

        with Status("[magenta]Sintetizando voz...[/magenta]"):
            self.tts.speak(answer)

        return text, answer

    def run_loop(self):
        """Bucle continuo para atender reunión completa."""
        console.print("\n[bold green]Agente activo[/bold green] — Ctrl+C para salir\n")
        self.claude.reset_history()

        try:
            while True:
                self.run_once()
        except KeyboardInterrupt:
            console.print("\n[dim]Sesión terminada.[/dim]")
