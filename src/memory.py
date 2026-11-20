"""Persistent, dependency-free conversation memory."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Any


@dataclass
class Message:
    role: str
    content: str


class Memory:
    def __init__(self, path: str | Path | None = None, max_messages: int = 40):
        self.path = Path(path) if path else None
        self.max_messages = max_messages
        self.messages: list[Message] = []
        if self.path:
            self.load()

    @property
    def history(self) -> list[str]:
        return [message.content for message in self.messages]

    def add(self, message: str, role: str = "user") -> None:
        self.messages.append(Message(role=role, content=message))
        self.messages = self.messages[-self.max_messages :]
        self.save()

    def get_recent(self, n: int = 5) -> list[str]:
        return [message.content for message in self.messages[-n:]]

    def as_dicts(self, n: int | None = None) -> list[dict[str, str]]:
        messages = self.messages[-n:] if n else self.messages
        return [asdict(message) for message in messages]

    def clear(self) -> None:
        self.messages = []
        self.save()

    def load(self) -> None:
        if not self.path or not self.path.exists():
            return
        try:
            raw: Any = json.loads(self.path.read_text(encoding="utf-8"))
            self.messages = [Message(**item) for item in raw if item.get("role") and item.get("content")]
        except (OSError, json.JSONDecodeError, TypeError):
            self.messages = []

    def save(self) -> None:
        if not self.path:
            return
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(self.as_dicts(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
