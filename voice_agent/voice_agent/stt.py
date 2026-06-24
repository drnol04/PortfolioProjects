"""Speech-to-Text usando faster-whisper (local) con fallback a Google Speech Recognition."""

import io
import queue
import wave
import numpy as np
import sounddevice as sd
from voice_agent.config import cfg


class SpeechToText:
    def __init__(self):
        self.sample_rate = cfg["audio"]["sample_rate"]
        self.silence_timeout = cfg["agent"]["silence_timeout"]
        self._audio_queue: queue.Queue = queue.Queue()
        self._recording = False
        self._model = None
        self._backend = self._init_backend()

    def _init_backend(self) -> str:
        try:
            from faster_whisper import WhisperModel
            stt_cfg = cfg.get("stt", {})
            self._model = WhisperModel(
                stt_cfg.get("model", "base"),
                device=stt_cfg.get("device", "cpu"),
                compute_type=stt_cfg.get("compute_type", "int8"),
            )
            return "faster-whisper"
        except Exception:
            pass

        try:
            import speech_recognition  # noqa: F401
            return "google"
        except Exception:
            pass

        raise RuntimeError(
            "No STT backend available. "
            "Install faster-whisper: pip install faster-whisper\n"
            "Or Google SR fallback: pip install SpeechRecognition"
        )

    def _audio_callback(self, indata, frames, time, status):
        if self._recording:
            self._audio_queue.put(indata.copy())

    def record_until_silence(self) -> np.ndarray | None:
        """Graba hasta detectar silencio usando VAD simple por energía."""
        try:
            import webrtcvad
            vad = webrtcvad.Vad(2)
            use_vad = True
        except Exception:
            use_vad = False

        chunks: list[np.ndarray] = []
        silent_chunks = 0
        speaking_started = False
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

                if use_vad:
                    pcm = chunk.flatten().tobytes()
                    is_speech = vad.is_speech(pcm, self.sample_rate)
                else:
                    rms = np.sqrt(np.mean(chunk.astype(np.float32) ** 2))
                    is_speech = rms > 300

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

        return np.concatenate(chunks, axis=0).flatten()

    def _audio_to_wav_bytes(self, audio_int16: np.ndarray) -> bytes:
        buf = io.BytesIO()
        with wave.open(buf, "wb") as wf:
            wf.setnchannels(cfg["audio"]["channels"])
            wf.setsampwidth(2)
            wf.setframerate(self.sample_rate)
            wf.writeframes(audio_int16.tobytes())
        return buf.getvalue()

    def _transcribe_faster_whisper(self, audio_int16: np.ndarray) -> str:
        audio_float32 = audio_int16.astype(np.float32) / 32768.0
        lang = cfg["agent"]["language"]
        language = None if lang == "auto" else lang
        segments, _ = self._model.transcribe(audio_float32, language=language)
        return " ".join(seg.text for seg in segments).strip()

    def _transcribe_google(self, audio_int16: np.ndarray) -> str:
        import speech_recognition as sr
        wav_bytes = self._audio_to_wav_bytes(audio_int16)
        recognizer = sr.Recognizer()
        with sr.AudioFile(io.BytesIO(wav_bytes)) as source:
            audio_data = recognizer.record(source)
        lang = cfg["agent"]["language"]
        language = "es-ES" if lang == "es" else ("en-US" if lang == "en" else "es-ES")
        return recognizer.recognize_google(audio_data, language=language)

    def transcribe(self, audio_int16: np.ndarray) -> str:
        if self._backend == "faster-whisper":
            return self._transcribe_faster_whisper(audio_int16)
        return self._transcribe_google(audio_int16)

    def listen(self) -> str | None:
        """Graba y transcribe en un solo paso. Retorna el texto o None."""
        audio = self.record_until_silence()
        if audio is None or len(audio) < self.sample_rate * 0.5:
            return None
        return self.transcribe(audio) or None
