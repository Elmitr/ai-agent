from pathlib import Path

from src.agent import Agent
from src.executor import execute_step
from src.memory import Memory
from src.planner import plan_task
from src.tools.builtin import calculate


def test_calculator_is_safe_and_correct():
    assert calculate("2 + 3 * 4") == "14"
    assert calculate("sqrt(16)") == "4"


def test_calculator_rejects_code():
    try:
        calculate("__import__('os').system('echo bad')")
    except ValueError:
        pass
    else:
        raise AssertionError("unsafe expression was accepted")


def test_memory_persists(tmp_path: Path):
    path = tmp_path / "memory.json"
    memory = Memory(path)
    memory.add("hello")
    memory.add("world", role="assistant")
    restored = Memory(path)
    assert restored.get_recent(2) == ["hello", "world"]
    assert restored.as_dicts(1)[0]["role"] == "assistant"


def test_offline_plan_and_execution():
    steps = plan_task("احسب 10 / 2", client=None)
    assert steps[0]["tool"] == "calculate"
    result = execute_step(steps[0])
    assert result.ok is True
    assert result.output == "5"


def test_agent_runs_without_api_key(tmp_path: Path):
    agent = Agent(memory=Memory(tmp_path / "memory.json"))
    result = agent.run("احسب 7 * 6")
    assert result.answer == "42"
    assert result.used_llm is False
