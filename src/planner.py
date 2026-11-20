"""Task planning for the agent."""

from __future__ import annotations

import json
import re
from typing import Any

from .tools.gemini_tool import GeminiClient


def _fallback_plan(user_input: str) -> list[dict[str, Any]]:
    text = user_input.lower()
    if any(token in text for token in ("احسب", "calculate", "+", "-", "*", "/")):
        expression = re.sub(r"[^0-9۰-۹٠-٩+*/%.() -]", "", user_input)
        expression = expression.strip()
        return [{"kind": "tool", "tool": "calculate", "input": expression or user_input}]
    if any(token in text for token in ("الوقت", "الساعة", "time")):
        return [{"kind": "tool", "tool": "current_time", "input": {"timezone": "UTC"}}]
    if any(token in text for token in ("لخص", "تلخيص", "summarize")):
        return [{"kind": "tool", "tool": "summarize_text", "input": user_input}]
    return [{"kind": "respond", "input": user_input}]


def plan_task(user_input: str, client: GeminiClient | None = None) -> list[dict[str, Any]]:
    """Return a small, validated plan; never expose arbitrary Python execution."""
    client = client or GeminiClient()
    if not client.available:
        return _fallback_plan(user_input)
    prompt = f"""أنت مخطط مهام لوكيل ذكاء اصطناعي.
أعد JSON فقط بهذا الشكل: {{"steps":[{{"kind":"tool|respond","tool":"...","input":...}}]}}
الأدوات المسموح بها: calculate, current_time, summarize_text.
لا تنشئ أكثر من 4 خطوات ولا تستخدم أدوات غير القائمة.
طلب المستخدم: {user_input}
"""
    try:
        data = client.call_json(prompt)
        steps = data.get("steps", [])
        if not isinstance(steps, list) or not steps or len(steps) > 4:
            raise ValueError("invalid plan length")
        valid = []
        for step in steps:
            if not isinstance(step, dict) or step.get("kind") not in {"tool", "respond"}:
                raise ValueError("invalid step")
            if step["kind"] == "tool" and step.get("tool") not in {"calculate", "current_time", "summarize_text"}:
                raise ValueError("unknown tool")
            valid.append(step)
        return valid
    except (ValueError, TypeError, json.JSONDecodeError, RuntimeError):
        return _fallback_plan(user_input)
