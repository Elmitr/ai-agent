"""Thin Gemini adapter with a deterministic offline fallback."""

from __future__ import annotations

import json
import os
from typing import Any

from dotenv import load_dotenv

load_dotenv()


class GeminiClient:
    def __init__(self, api_key: str | None = None, model_name: str | None = None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY", "")
        self.model_name = model_name or os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        self._model: Any = None
        if self.api_key:
            try:
                import google.generativeai as genai

                genai.configure(api_key=self.api_key)
                self._model = genai.GenerativeModel(self.model_name)
            except ImportError:
                self._model = None

    @property
    def available(self) -> bool:
        return self._model is not None

    def call(self, prompt: str) -> str:
        if not self._model:
            raise RuntimeError("Gemini غير متاح: تحقق من GOOGLE_API_KEY وتثبيت الحزمة")
        response = self._model.generate_content(prompt)
        text = getattr(response, "text", None)
        if not text:
            raise RuntimeError("لم يُرجع Gemini نصًا")
        return text.strip()

    def call_json(self, prompt: str) -> dict[str, Any]:
        text = self.call(prompt).strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0]
        value = json.loads(text)
        if not isinstance(value, dict):
            raise ValueError("استجابة Gemini ليست كائن JSON")
        return value


_default_client = GeminiClient()


def call_gemini(prompt: str) -> str:
    """Backward-compatible helper used by small integrations."""
    return _default_client.call(prompt)
