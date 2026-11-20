"""Execute only registered tools."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .tools.builtin import ToolError, tool_registry


@dataclass
class StepResult:
    ok: bool
    output: str
    tool: str | None = None


def execute_step(step: dict[str, Any], registry: dict[str, Any] | None = None) -> StepResult:
    if step.get("kind") == "respond":
        return StepResult(ok=True, output=str(step.get("input", "")))
    tool_name = step.get("tool")
    registry = registry or tool_registry()
    tool = registry.get(tool_name)
    if not tool:
        return StepResult(ok=False, output=f"الأداة غير مسموحة: {tool_name}", tool=tool_name)
    raw_input = step.get("input", {})
    try:
        if isinstance(raw_input, dict):
            output = tool(**raw_input)
        elif tool_name == "calculate":
            output = tool(str(raw_input))
        elif tool_name == "summarize_text":
            output = tool(str(raw_input))
        else:
            output = tool()
        return StepResult(ok=True, output=str(output), tool=tool_name)
    except (ToolError, TypeError, ValueError, ZeroDivisionError) as exc:
        return StepResult(ok=False, output=f"فشل تنفيذ {tool_name}: {exc}", tool=tool_name)
