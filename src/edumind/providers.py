"""Model-provider boundary.

Only the protocol is provider-specific. The local adapter keeps this repository
fully runnable without network access or credentials.
"""

from typing import Any, Mapping, Protocol, Sequence

from .schemas import LessonRequest, RetrievedEvidence


class LLMProvider(Protocol):
    def generate(
        self, request: LessonRequest, evidence: Sequence[RetrievedEvidence]
    ) -> Mapping[str, Any]: ...


class DemoProvider:
    """Deterministic fallback used by the runnable example."""

    def generate(
        self, request: LessonRequest, evidence: Sequence[RetrievedEvidence]
    ) -> Mapping[str, Any]:
        topic = request.topic
        return {
            "objectives": (
                f"Explain the core concepts of {topic}.",
                "Interpret one representation and justify a prediction.",
            ),
            "sequence": (
                "Activate prior knowledge (5 min)",
                "Evidence-grounded mini lesson (15 min)",
                "Collaborative prediction task (15 min)",
                "Exit ticket and feedback (10 min)",
            ),
            "activities": (
                f"Predict an outcome related to {topic}.",
                "Compare predictions with the retrieved evidence.",
            ),
            "assessment": (
                "State the main claim in one sentence.",
                "Solve a transfer question and explain the reasoning.",
            ),
        }

