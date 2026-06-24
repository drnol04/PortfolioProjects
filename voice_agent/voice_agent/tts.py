"""Text-to-Speech con voz clonada via ElevenLabs."""

import io
import sounddevice as sd
import soundfile as sf
import numpy as np
from voice_agent.config import cfg, ELEVENLABS_API_KEY, ELEVENLABS_VOICE_ID


class TextToSpeech:
    def __init__(self):
        self.provider = cfg["tts"]["provider"]
        self._el_client = None

        if self.provider == "elevenlabs":
            if not ELEVENLABS_API_KEY:
                raise ValueError("ELEVENLABS_API_KEY no configurada en .env")
            from elevenlabs import ElevenLabs
            self._el_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

        self.sample_rate = cfg["audio"]["sample_rate"]
        self._output_device = cfg["audio"].get("output_device")

    def synthesize(self, text: str) -> bytes:
        """Genera audio MP3 a partir de texto."""
        if self.provider == "elevenlabs":
            return self._synthesize_elevenlabs(text)
        return self._synthesize_system(text)

    def _synthesize_elevenlabs(self, text: str) -> bytes:
        tts_cfg = cfg["tts"]
        voice_id = ELEVENLABS_VOICE_ID or tts_cfg.get("voice_id", "")
        if not voice_id:
            raise ValueError(
                "ELEVENLABS_VOICE_ID no configurado. "
                "Clona tu voz en elevenlabs.io y pega el Voice ID en .env"
            )
        audio = self._el_client.text_to_speech.convert(
            voice_id=voice_id,
            text=text,
            model_id=tts_cfg["model"],
            voice_settings={
                "stability": tts_cfg["stability"],
                "similarity_boost": tts_cfg["similarity_boost"],
            },
            output_format="mp3_44100_128",
        )
        return b"".join(audio)

    def _synthesize_system(self, text: str) -> bytes:
        # Fallback: pyttsx3 sin clonar voz
        try:
            import pyttsx3, tempfile, os
            engine = pyttsx3.init()
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                path = f.name
            engine.save_to_file(text, path)
            engine.runAndWait()
            with open(path, "rb") as f:
                data = f.read()
            os.unlink(path)
            return data
        except Exception as e:
            raise RuntimeError(f"Sistema TTS falló: {e}")

    def speak(self, text: str):
        """Sintetiza y reproduce el audio inmediatamente."""
        audio_bytes = self.synthesize(text)
        data, sr = sf.read(io.BytesIO(audio_bytes))
        sd.play(data, samplerate=sr, device=self._output_device)
        sd.wait()

    def speak_to_virtual_device(self, text: str, device_name: str):
        """Reproduce en un dispositivo de audio virtual (para Zoom)."""
        audio_bytes = self.synthesize(text)
        data, sr = sf.read(io.BytesIO(audio_bytes))

        # Busca el índice del dispositivo virtual por nombre
        devices = sd.query_devices()
        device_idx = None
        for i, dev in enumerate(devices):
            if device_name.lower() in dev["name"].lower() and dev["max_output_channels"] > 0:
                device_idx = i
                break

        if device_idx is None:
            raise ValueError(f"Dispositivo virtual '{device_name}' no encontrado. Dispositivos disponibles:\n" +
                             "\n".join(f"  [{i}] {d['name']}" for i, d in enumerate(devices)))

        sd.play(data, samplerate=sr, device=device_idx)
        sd.wait()
