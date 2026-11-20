"""Command-line entry point for the practical agent."""

from __future__ import annotations

import argparse

from .agent import Agent
from .config import settings


def main() -> None:
    parser = argparse.ArgumentParser(description="Agentic AI assistant")
    parser.add_argument("prompt", nargs="*", help="طلب واحد؛ اتركه فارغًا للدخول إلى المحادثة")
    parser.add_argument("--clear-memory", action="store_true", help="مسح الذاكرة المحلية")
    args = parser.parse_args()

    agent = Agent()
    if args.clear_memory:
        agent.memory.clear()
        print("تم مسح الذاكرة.")
        return
    if args.prompt:
        print(agent.run(" ".join(args.prompt)).answer)
        return

    print("وكيل الذكاء الاصطناعي جاهز. اكتب exit للخروج.")
    while True:
        try:
            question = input("\nأنت> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if question.lower() in {"exit", "quit", "خروج"}:
            break
        print(f"\nالوكيل> {agent.run(question).answer}")


if __name__ == "__main__":
    main()
