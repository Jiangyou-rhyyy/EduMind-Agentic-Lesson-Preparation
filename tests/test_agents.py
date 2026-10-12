import pytest

from edumind.agents import PlannerAgent, VerifierAgent
from edumind.providers import DemoProvider
from edumind.schemas import LessonRequest, RetrievedEvidence, KnowledgeChunk


def _evidence():
    return (
        RetrievedEvidence(
            chunk=KnowledgeChunk("physics-free-fall", "Free Fall", "Acceleration is constant."),
            score=1.0,
        ),
    )


def test_demo_provider_is_deterministic_and_provider_agnostic():
    request = LessonRequest(topic="Free fall", grade="10", duration_minutes=45)
    planner = PlannerAgent(DemoProvider())
    first = planner.plan(request, _evidence())
    second = planner.plan(request, _evidence())
    assert first == second
    assert first.objectives
    assert first.evidence == ("physics-free-fall",)


def test_verifier_reports_missing_evidence_as_failure():
    request = LessonRequest(topic="Free fall", grade="10", duration_minutes=45)
    plan = PlannerAgent(DemoProvider()).plan(request, ())
    report = VerifierAgent().verify(plan)
    assert not report.passed
    assert "evidence" in report.checks


def test_provider_output_must_use_non_empty_string_sequences():
    class MalformedProvider:
        def generate(self, request, evidence):
            return {"objectives": "one string", "sequence": (), "activities": (), "assessment": ()}

    request = LessonRequest(topic="Free fall", grade="10", duration_minutes=45)
    with pytest.raises(ValueError, match="objectives"):
        PlannerAgent(MalformedProvider()).plan(request, _evidence())


def test_verifier_rejects_sequence_with_wrong_total_duration():
    request = LessonRequest(topic="Free fall", grade="10", duration_minutes=60)
    plan = PlannerAgent(DemoProvider()).plan(request, _evidence())
    assert sum(int(item.split("(")[1].split(" ")[0]) for item in plan.sequence) == 60
    assert VerifierAgent().verify(plan).passed
