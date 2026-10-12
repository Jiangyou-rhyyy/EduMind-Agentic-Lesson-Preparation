"""Role-oriented agents for the lesson preparation pipeline."""

from typing import Sequence

from .providers import LLMProvider, ProviderDraft
from .schemas import (
    LessonPlan,
    LessonRequest,
    RetrievedEvidence,
    VerificationReport,
)


class ResearchAgent:
    def retrieve(self, query: str, store, top_k: int = 4) -> tuple[RetrievedEvidence, ...]:
        return store.search(query, top_k=top_k)


class PlannerAgent:
    def __init__(self, provider: LLMProvider):
        self.provider = provider

    def plan(
        self, request: LessonRequest, evidence: Sequence[RetrievedEvidence]
    ) -> LessonPlan:
        draft = ProviderDraft.from_mapping(self.provider.generate(request, evidence))
        return LessonPlan(
            request=request,
            objectives=draft.objectives,
            sequence=draft.sequence,
            activities=draft.activities,
            assessment=draft.assessment,
            evidence=tuple(item.chunk.source_id for item in evidence),
        )


class VerifierAgent:
    def verify(self, plan: LessonPlan) -> VerificationReport:
        checks: list[str] = []
        warnings: list[str] = []
        if plan.objectives:
            checks.append("objectives")
        else:
            warnings.append("No learning objectives were generated.")
        durations = []
        for step in plan.sequence:
            marker = step.rsplit("(", 1)[-1].removesuffix(" min)")
            if marker.isdigit():
                durations.append(int(marker))
        if plan.sequence and sum(durations) == plan.request.duration_minutes:
            checks.append("timing")
        else:
            warnings.append("Lesson sequence timing does not match the requested duration.")
        if plan.activities and plan.assessment:
            checks.append("assessment")
        else:
            warnings.append("Activities and assessment should both be present.")
        if plan.evidence:
            checks.append("evidence")
        else:
            checks.append("evidence")
            warnings.append("No retrieved evidence was attached.")
        passed = not warnings
        return VerificationReport(
            plan=plan,
            passed=passed,
            checks=tuple(checks),
            warnings=tuple(warnings),
        )

