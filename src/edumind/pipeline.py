"""Orchestration boundary for the retrieval-to-plan workflow."""

from dataclasses import dataclass

from .agents import PlannerAgent, ResearchAgent, VerifierAgent
from .providers import LLMProvider
from .schemas import LessonPlan, LessonRequest, VerificationReport


@dataclass(frozen=True)
class PipelineResult:
    plan: LessonPlan
    report: VerificationReport


class LessonPreparationPipeline:
    def __init__(self, store, provider: LLMProvider):
        self.research = ResearchAgent()
        self.planner = PlannerAgent(provider)
        self.verifier = VerifierAgent()
        self.store = store

    def run(self, request: LessonRequest, top_k: int = 4) -> PipelineResult:
        evidence = self.research.retrieve(request.topic, self.store, top_k=top_k)
        plan = self.planner.plan(request, evidence)
        report = self.verifier.verify(plan)
        return PipelineResult(plan=plan, report=report)

