import json
from pathlib import Path

from edumind.knowledge import KnowledgeStore, load_markdown_directory
from edumind.pipeline import LessonPreparationPipeline
from edumind.providers import DemoProvider
from edumind.render import plan_to_json, plan_to_markdown
from edumind.schemas import LessonRequest


def test_pipeline_returns_verified_plan_with_provenance():
    store = KnowledgeStore(load_markdown_directory(Path("data/knowledge")))
    result = LessonPreparationPipeline(store, DemoProvider()).run(
        LessonRequest(topic="free fall", grade="10", duration_minutes=45)
    )
    assert result.report.passed
    assert result.report.plan.evidence == ("physics-free-fall",)


def test_renderers_are_stable_and_machine_readable():
    store = KnowledgeStore(load_markdown_directory(Path("data/knowledge")))
    result = LessonPreparationPipeline(store, DemoProvider()).run(
        LessonRequest(topic="free fall", grade="10", duration_minutes=45)
    )
    markdown = plan_to_markdown(result.report)
    payload = json.loads(plan_to_json(result.report))
    assert "# Lesson Plan: free fall" in markdown
    assert payload["verification"]["passed"] is True
