#!/usr/bin/env python3
"""
Voice Agent para Zoom - CLI principal.

Comandos:
  ingest   - Indexa los documentos en ./documents/
  run      - Inicia el agente de voz en modo bucle
  devices  - Lista dispositivos de audio disponibles
  test     - Prueba STT + Claude + TTS con una sola pregunta
"""

import typer
from pathlib import Path
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="Agente de voz para reuniones Zoom con Claude + documentos propios")
console = Console()


@app.command()
def ingest(
    path: Path = typer.Argument(None, help="Archivo específico o deja vacío para procesar ./documents/")
):
    """Indexa tus documentos en la base vectorial."""
    from voice_agent.rag import DocumentStore

    console.print("[cyan]Indexando documentos...[/cyan]")
    store = DocumentStore()
    count = store.ingest(path)
    if count:
        console.print(f"[green]✓ {count} fragmentos indexados correctamente.[/green]")
    else:
        console.print("[yellow]No se encontraron documentos. Agrega archivos a ./documents/[/yellow]")
        console.print("Formatos soportados: PDF, DOCX, TXT, MD, XLSX, CSV")


@app.command()
def run():
    """Inicia el agente de voz en modo bucle para una reunión completa."""
    from voice_agent.agent import VoiceAgent
    agent = VoiceAgent()
    agent.run_loop()


@app.command()
def test(question: str = typer.Argument("¿Cuáles son los temas principales de mis documentos?")):
    """Prueba el agente con una pregunta de texto (sin usar micrófono)."""
    from voice_agent.rag import DocumentStore
    from voice_agent.claude_agent import ClaudeAgent
    from voice_agent.tts import TextToSpeech

    console.print(f"[bold white]Pregunta:[/bold white] {question}")

    store = DocumentStore()
    agent = ClaudeAgent(store)
    answer = agent.answer(question)
    console.print(f"[bold green]Respuesta:[/bold green] {answer}")

    console.print("\n[cyan]Reproduciendo voz...[/cyan]")
    tts = TextToSpeech()
    tts.speak(answer)


@app.command()
def devices():
    """Lista todos los dispositivos de audio disponibles en tu sistema."""
    import sounddevice as sd

    all_devs = sd.query_devices()
    table = Table(title="Dispositivos de Audio", show_header=True)
    table.add_column("#", style="dim", width=4)
    table.add_column("Nombre", style="cyan")
    table.add_column("Entradas", justify="right")
    table.add_column("Salidas", justify="right")
    table.add_column("Default", justify="center")

    default_in = sd.default.device[0]
    default_out = sd.default.device[1]

    for i, dev in enumerate(all_devs):
        is_default = ""
        if i == default_in:
            is_default += "IN "
        if i == default_out:
            is_default += "OUT"
        table.add_row(
            str(i),
            dev["name"],
            str(int(dev["max_input_channels"])),
            str(int(dev["max_output_channels"])),
            is_default.strip() or "-",
        )

    console.print(table)
    console.print("\n[dim]Configura el dispositivo en config.yaml → audio.input_device / output_device[/dim]")
    console.print("[dim]Para Zoom: usa el nombre del dispositivo virtual (VB-Cable, BlackHole, etc.)[/dim]")


@app.command()
def clone_guide():
    """Muestra las instrucciones para clonar tu voz en ElevenLabs."""
    console.print("""
[bold cyan]Guía para clonar tu voz con ElevenLabs[/bold cyan]

1. Crea una cuenta en [link]https://elevenlabs.io[/link]
2. Ve a Voices → Add Voice → Instant Voice Cloning
3. Graba o sube 1-5 minutos de audio de tu voz (MP3 o WAV)
   - Usa un ambiente silencioso
   - Habla con tono natural y variado
4. Copia el [bold]Voice ID[/bold] que aparece en la voz creada
5. Agrega al archivo .env:

   [green]ELEVENLABS_API_KEY=tu_api_key_aquí
   ELEVENLABS_VOICE_ID=tu_voice_id_aquí[/green]

6. Ejecuta: [bold]python main.py test[/bold] para verificar

[yellow]Nota:[/yellow] El plan gratuito de ElevenLabs incluye 10,000 caracteres/mes.
Para reuniones largas considera el plan Creator ($22/mes).
""")


if __name__ == "__main__":
    app()
