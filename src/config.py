"""Application configuration loaded from environment variables."""

from dataclasses import dataclass
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    google_api_key: str = os.getenv("GOOGLE_API_KEY", "")
    model_name: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    memory_path: Path = Path(os.getenv("AGENT_MEMORY_PATH", "data/memory.json"))
    max_turns: int = int(os.getenv("AGENT_MAX_TURNS", "6"))

    @property
    def has_llm(self) -> bool:
        return bool(self.google_api_key)


settings = Settings()
