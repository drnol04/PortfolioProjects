# Agente de Voz para Zoom

Agente de IA que usa **tu propia voz clonada** para responder preguntas en reuniones de Zoom, conectado a tus documentos y a Claude.

## Arquitectura

```
Reunión Zoom
    │
    ▼ (audio de participantes)
┌─────────────────────────────────────────────────────────┐
│                   AGENTE DE VOZ                          │
│                                                          │
│  Micrófono/Audio Virtual                                 │
│       │                                                  │
│       ▼                                                  │
│  ┌─────────┐    ┌──────────┐    ┌────────────────────┐  │
│  │ Whisper │───▶│  Claude  │◀───│  Tus Documentos    │  │
│  │  (STT)  │    │   API    │    │  (RAG / ChromaDB)  │  │
│  └─────────┘    └────┬─────┘    └────────────────────┘  │
│                      │                                   │
│                      ▼                                   │
│               ┌─────────────┐                            │
│               │ ElevenLabs  │  (Tu voz clonada)          │
│               │    (TTS)    │                            │
│               └──────┬──────┘                            │
│                      │                                   │
└──────────────────────┼──────────────────────────────────┘
                       │ (audio virtual → Zoom)
                       ▼
              Participantes escuchan
              tu voz respondiendo
```

## Instalación

### 1. Clonar y preparar entorno

```bash
cd voice_agent
python -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

### 2. Configurar claves API

```bash
cp .env.example .env
# Edita .env con tus claves:
# - ANTHROPIC_API_KEY
# - ELEVENLABS_API_KEY
# - ELEVENLABS_VOICE_ID
```

### 3. Clonar tu voz (ElevenLabs)

```bash
python main.py clone-guide
```

Sigue las instrucciones y pega el Voice ID en `.env`.

### 4. Configurar audio virtual para Zoom

**Linux:**
```bash
bash scripts/setup_virtual_audio_linux.sh
```

**macOS:**
```bash
bash scripts/setup_virtual_audio_mac.sh
```

**Windows:** Ver `scripts/setup_virtual_audio_windows.md`

### 5. Indexar tus documentos

Copia tus archivos (PDF, Word, Excel, TXT) a la carpeta `documents/` y ejecuta:

```bash
python main.py ingest
```

Formatos soportados: **PDF, DOCX, TXT, MD, XLSX, CSV**

## Uso

### Iniciar agente en una reunión

```bash
python main.py run
```

El agente:
1. Escucha cuando alguien habla (detección de silencio automática)
2. Transcribe la pregunta con Whisper
3. Busca contexto en tus documentos
4. Genera respuesta con Claude
5. Habla con tu voz clonada por el dispositivo virtual

### Probar sin micrófono

```bash
python main.py test "¿Cuál es el presupuesto del proyecto X?"
```

### Ver dispositivos de audio

```bash
python main.py devices
```

## Configuración avanzada

Edita `config.yaml` para ajustar:

- `agent.language`: idioma de transcripción (`es`, `en`, `auto`)
- `stt.model`: tamaño del modelo Whisper (`tiny` < `base` < `small` < `medium` < `large-v3`)
- `audio.input_device` / `audio.output_device`: dispositivos de audio
- `claude.system_prompt`: personalidad y contexto del agente
- `rag.top_k`: cuántos fragmentos de documentos usar como contexto

## Flujo de una reunión típica

1. Abre Zoom y configura el micrófono como el dispositivo virtual
2. Ejecuta `python main.py run`
3. Cuando alguien te haga una pregunta, el agente la escucha y responde automáticamente
4. Presiona `Ctrl+C` al terminar la reunión

## Requisitos

- Python 3.10+
- [Anthropic API key](https://console.anthropic.com)
- [ElevenLabs API key](https://elevenlabs.io) (plan gratuito: 10k chars/mes)
- Dispositivo de audio virtual instalado (VB-Cable / BlackHole / PulseAudio)
