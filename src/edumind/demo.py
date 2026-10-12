"""Command-line entry point for the offline EduMind demonstration."""

import argparse
from pathlib import Path
from typing import Sequence

from .knowledge import KnowledgeStore, load_markdown_directory
from .pipeline import LessonPreparationPipeline
from .providers import DemoProvider
from .render import plan_to_json, plan_to_markdown
from .schemas import LessonRequest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the EduMind lesson preparation demo.")
    parser.add_argument("--topic", default="free fall")
    parser.add_argument("--grade", default="10")
    parser.add_argument("--duration", type=int, default=45)
    parser.add_argument(
        "--knowledge-dir",
        type=Path,
        default=Path(__file__).resolve().parents[2] / "data" / "knowledge",
    )
    parser.add_argument("--markdown-output", type=Path)
    parser.add_argument("--json-output", type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        store = KnowledgeStore(load_markdown_directory(args.knowledge_dir))
    except FileNotFoundError as exc:
        build_parser().error(str(exc))
    request = LessonRequest(topic=args.topic, grade=args.grade, duration_minutes=args.duration)
    result = LessonPreparationPipeline(store, DemoProvider()).run(request)
    markdown = plan_to_markdown(result.report)
    payload = plan_to_json(result.report)
    if args.markdown_output:
        args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
        args.markdown_output.write_text(markdown, encoding="utf-8")
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(payload + "\n", encoding="utf-8")
    if not args.markdown_output and not args.json_output:
        print(markdown, end="")
    return 0 if result.report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

