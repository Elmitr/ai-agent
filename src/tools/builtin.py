"""Small deterministic tools exposed to the agent."""

from __future__ import annotations

import ast
import datetime as dt
import math
import operator
from typing import Callable


class ToolError(ValueError):
    """Raised when a tool receives invalid input."""


_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
}
_UNARY_OPS = {ast.UAdd: operator.pos, ast.USub: operator.neg}


def _eval(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.BinOp) and type(node.op) in _BIN_OPS:
        left, right = _eval(node.left), _eval(node.right)
        if isinstance(node.op, ast.Pow) and abs(right) > 100:
            raise ToolError("exponent is too large")
        return _BIN_OPS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPS:
        return _UNARY_OPS[type(node.op)](_eval(node.operand))
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        allowed = {"sqrt": math.sqrt, "abs": abs, "round": round}
        if node.func.id in allowed and len(node.keywords) == 0:
            return float(allowed[node.func.id](*[_eval(arg) for arg in node.args]))
    raise ToolError("unsupported expression")


def calculate(expression: str) -> str:
    """Evaluate a numeric expression without using eval()."""
    if not expression or len(expression) > 200:
        raise ToolError("expression is empty or too long")
    try:
        value = _eval(ast.parse(expression, mode="eval").body)
    except (SyntaxError, ValueError, ZeroDivisionError, OverflowError, TypeError) as exc:
        raise ToolError(f"invalid expression: {exc}") from exc
    return str(int(value)) if value.is_integer() else str(value)


def current_time(timezone: str = "UTC") -> str:
    """Return an ISO timestamp; timezone support stays dependency-free."""
    if timezone.upper() != "UTC":
        raise ToolError("only UTC is supported by the built-in time tool")
    return dt.datetime.now(dt.timezone.utc).isoformat()


def summarize_text(text: str, max_words: int = 80) -> str:
    """Provide a deterministic fallback summary when no LLM is configured."""
    words = (text or "").split()
    if not words:
        return "لا يوجد نص لتلخيصه."
    if len(words) <= max_words:
        return " ".join(words)
    return " ".join(words[:max_words]) + " …"


def tool_registry() -> dict[str, Callable[..., str]]:
    return {
        "calculate": calculate,
        "current_time": current_time,
        "summarize_text": summarize_text,
    }


def tool_descriptions() -> list[dict[str, str]]:
    return [
        {"name": "calculate", "description": "حساب تعبير رياضي رقمي آمن."},
        {"name": "current_time", "description": "إرجاع الوقت الحالي بصيغة ISO؛ يدعم UTC."},
        {"name": "summarize_text", "description": "تلخيص نص بطريقة احتياطية محلية."},
    ]
