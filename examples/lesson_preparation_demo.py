"""Minimal library-level invocation of the EduMind pipeline."""

from pathlib import Path

from edumind.knowledge import KnowledgeStore, load_markdown_directory
from edumind.pipeline import LessonPreparationPipeline
from edumind.providers import DemoProvider
from edumind.render import plan_to_markdown
from edumind.schemas import LessonRequest


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    store = KnowledgeStore(load_markdown_directory(root / "data" / "knowledge"))
    result = LessonPreparationPipeline(store, DemoProvider()).run(
        LessonRequest(topic="free fall", grade="10", duration_minutes=45)
    )
    print(plan_to_markdown(result.report))


if __name__ == "__main__":
    main()

