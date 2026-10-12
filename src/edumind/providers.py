"""Model-provider boundary.

Only the protocol is provider-specific. The local adapter keeps this repository
fully runnable without network access or credentials.
"""

from dataclasses import dataclass
from typing import Any, Mapping, Protocol, Sequence

from .schemas import LessonRequest, RetrievedEvidence


class LLMProvider(Protocol):
    def generate(
        self, request: LessonRequest, evidence: Sequence[RetrievedEvidence]
    ) -> Mapping[str, Any]: ...


def _string_sequence(value: object, field: str) -> tuple[str, ...]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise ValueError(f"provider field '{field}' must be a sequence of non-empty strings")
    items = tuple(item.strip() if isinstance(item, str) else "" for item in value)
    if any(not item for item in items):
        raise ValueError(f"provider field '{field}' must be a sequence of non-empty strings")
    return items


@dataclass(frozen=True)
class ProviderDraft:
    objectives: tuple[str, ...]
    sequence: tuple[str, ...]
    activities: tuple[str, ...]
    assessment: tuple[str, ...]

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "ProviderDraft":
        if not isinstance(value, Mapping):
            raise ValueError("provider output must be a mapping")
        return cls(
            objectives=_string_sequence(value.get("objectives", ()), "objectives"),
            sequence=_string_sequence(value.get("sequence", ()), "sequence"),
            activities=_string_sequence(value.get("activities", ()), "activities"),
            assessment=_string_sequence(value.get("assessment", ()), "assessment"),
        )


class DemoProvider:
    """Deterministic fallback used by the runnable example."""

    def generate(
        self, request: LessonRequest, evidence: Sequence[RetrievedEvidence]
    ) -> Mapping[str, Any]:
        topic = request.topic
        weights = (0.10, 0.35, 0.35, 0.20)
        exact = [request.duration_minutes * weight for weight in weights]
        minutes = [int(value) for value in exact]
        for index in sorted(range(len(exact)), key=lambda item: exact[item] - minutes[item], reverse=True):
            if sum(minutes) >= request.duration_minutes:
                break
            minutes[index] += 1
        sequence = (
            f"Activate prior knowledge ({minutes[0]} min)",
            f"Evidence-grounded mini lesson ({minutes[1]} min)",
            f"Collaborative prediction task ({minutes[2]} min)",
            f"Exit ticket and feedback ({minutes[3]} min)",
        )
        return {
            "objectives": (
                f"Explain the core concepts of {topic}.",
                "Interpret one representation and justify a prediction.",
            ),
            "sequence": sequence,
            "activities": (
                f"Predict an outcome related to {topic}.",
                "Compare predictions with the retrieved evidence.",
            ),
            "assessment": (
                "State the main claim in one sentence.",
                "Solve a transfer question and explain the reasoning.",
            ),
        }

