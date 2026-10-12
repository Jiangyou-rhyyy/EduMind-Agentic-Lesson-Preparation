from datetime import timedelta

import pytest

from edumind.schemas import (
    KnowledgeChunk,
    LessonPlan,
    LessonRequest,
    RetrievedEvidence,
    VerificationReport,
)


def test_lesson_request_rejects_blank_topic_and_non_positive_duration():
    with pytest.raises(ValueError, match="topic"):
        LessonRequest(topic="  ", grade="10", duration_minutes=45)

    with pytest.raises(ValueError, match="duration"):
        LessonRequest(topic="Free fall", grade="10", duration_minutes=0)


def test_retrieved_evidence_preserves_source_and_bounded_score():
    chunk = KnowledgeChunk(source_id="physics/free-fall", title="Free fall", text="Acceleration is constant.")
    evidence = RetrievedEvidence(chunk=chunk, score=0.8)
    assert evidence.chunk.source_id == "physics/free-fall"
    assert evidence.score == 0.8

    with pytest.raises(ValueError, match="score"):
        RetrievedEvidence(chunk=chunk, score=1.2)


def test_lesson_plan_contains_typed_sections_and_verification_summary():
    request = LessonRequest(topic="Free fall", grade="10", duration_minutes=45)
    plan = LessonPlan(
        request=request,
        objectives=("Explain constant acceleration",),
        sequence=("Warm-up", "Model", "Exit ticket"),
        activities=("Graph position over time",),
        assessment=("Predict the next position",),
        evidence=("physics/free-fall",),
    )
    report = VerificationReport(plan=plan, passed=True, checks=("objectives", "timing"))
    assert report.passed
    assert report.checks == ("objectives", "timing")
