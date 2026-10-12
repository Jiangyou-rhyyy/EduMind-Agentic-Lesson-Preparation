"""Small, serializable data contracts for the EduMind pipeline."""

from dataclasses import dataclass
from typing import Tuple


def _non_empty(value: str, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be non-empty")
    return value.strip()


@dataclass(frozen=True)
class LessonRequest:
    topic: str
    grade: str
    duration_minutes: int
    learning_constraints: Tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "topic", _non_empty(self.topic, "topic"))
        object.__setattr__(self, "grade", _non_empty(self.grade, "grade"))
        if self.duration_minutes <= 0:
            raise ValueError("duration must be positive")
        object.__setattr__(
            self,
            "learning_constraints",
            tuple(item.strip() for item in self.learning_constraints if item.strip()),
        )


@dataclass(frozen=True)
class KnowledgeChunk:
    source_id: str
    title: str
    text: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "source_id", _non_empty(self.source_id, "source_id"))
        object.__setattr__(self, "title", _non_empty(self.title, "title"))
        object.__setattr__(self, "text", _non_empty(self.text, "text"))


@dataclass(frozen=True)
class RetrievedEvidence:
    chunk: KnowledgeChunk
    score: float

    def __post_init__(self) -> None:
        if not 0.0 <= self.score <= 1.0:
            raise ValueError("score must be between 0 and 1")


@dataclass(frozen=True)
class LessonPlan:
    request: LessonRequest
    objectives: Tuple[str, ...]
    sequence: Tuple[str, ...]
    activities: Tuple[str, ...]
    assessment: Tuple[str, ...]
    evidence: Tuple[str, ...]


@dataclass(frozen=True)
class VerificationReport:
    plan: LessonPlan
    passed: bool
    checks: Tuple[str, ...]
    warnings: Tuple[str, ...] = ()

