"""Speech-to-Text usando Faster-Whisper (local, sin costo de API)."""

import io
import queue
import threading
import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel
from voice_agent.config import cfg


class SpeechToText:
    def __init__(self):
        stt_cfg = cfg["stt"]
        self.model = WhisperModel(
            stt_cfg["model"],
            device=stt_cfg["device"],
            compute_type=stt_cfg["compute_type"],
        )
        self.sample_rate = cfg["audio"]["sample_rate"]
        self.silence_timeout = cfg["agent"]["silence_timeout"]
        self._audio_queue: queue.Queue = queue.Queue()
        self._recording = False

    def _audio_callback(self, indata, frames, time, status):
        if self._recording:
            self._audio_queue.put(indata.copy())

    def record_until_silence(self) -> np.ndarray | None:
        """Graba audio hasta detectar silencio. Retorna array de audio."""
        import webrtcvad

        vad = webrtcvad.Vad(2)  # agresividad: 0-3
        chunks: list[np.ndarray] = []
        silent_chunks = 0
        speaking_started = False
        # 30ms por chunk a 16kHz = 480 samples
        frame_duration_ms = 30
        frame_samples = int(self.sample_rate * frame_duration_ms / 1000)

        self._recording = True
        self._audio_queue = queue.Queue()

        device = cfg["audio"].get("input_device")

        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=cfg["audio"]["channels"],
            dtype="int16",
            blocksize=frame_samples,
            device=device,
            callback=self._audio_callback,
        ):
            max_silent = int(self.silence_timeout * 1000 / frame_duration_ms)
            while True:
                chunk = self._audio_queue.get()
                pcm = chunk.flatten().tobytes()
                is_speech = vad.is_speech(pcm, self.sample_rate)

                if is_speech:
                    speaking_started = True
                    silent_chunks = 0
                    chunks.append(chunk)
                elif speaking_started:
                    chunks.append(chunk)
                    silent_chunks += 1
                    if silent_chunks >= max_silent:
                        break

        self._recording = False

        if not chunks:
            return None

        return np.concatenate(chunks, axis=0).flatten().astype(np.float32) / 32768.0

    def transcribe(self, audio: np.ndarray) -> str:
        """Transcribe un array de audio a texto."""
        segments, _ = self.model.transcribe(
            audio,
            language=cfg["agent"]["language"] if cfg["agent"]["language"] != "auto" else None,
            vad_filter=True,
        )
        return " ".join(seg.text.strip() for seg in segments).strip()

    def listen(self) -> str | None:
        """Graba y transcribe en un solo paso. Retorna el texto o None."""
        audio = self.record_until_silence()
        if audio is None or len(audio) < self.sample_rate * 0.3:
            return None
        return self.transcribe(audio) or None
