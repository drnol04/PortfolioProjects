import os
import yaml
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

_CONFIG_PATH = Path(__file__).parent.parent / "config.yaml"

def load_config() -> dict:
    with open(_CONFIG_PATH) as f:
        return yaml.safe_load(f)

cfg = load_config()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", cfg["tts"].get("voice_id", ""))
DOCUMENTS_DIR = Path(os.getenv("DOCUMENTS_DIR", Path(__file__).parent.parent / "documents"))
CHROMA_DIR = Path(__file__).parent.parent / cfg["rag"]["persist_directory"]
