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
