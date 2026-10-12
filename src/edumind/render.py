"""Stable serializers for CLI and downstream integrations."""

from dataclasses import asdict
import json

from .schemas import VerificationReport


def plan_to_json(report: VerificationReport) -> str:
    return json.dumps(
        {
            "plan": asdict(report.plan),
            "verification": {
                "passed": report.passed,
                "checks": report.checks,
                "warnings": report.warnings,
            },
        },
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    )


def _bullets(items: tuple[str, ...]) -> str:
    return "\n".join(f"- {item}" for item in items) or "- None"


def plan_to_markdown(report: VerificationReport) -> str:
    plan = report.plan
    lines = [
        f"# Lesson Plan: {plan.request.topic}",
        "",
        f"- **Grade:** {plan.request.grade}",
        f"- **Duration:** {plan.request.duration_minutes} minutes",
        f"- **Verification:** {'passed' if report.passed else 'needs review'}",
        "",
        "## Learning Objectives",
        _bullets(plan.objectives),
        "",
        "## Lesson Sequence",
        _bullets(plan.sequence),
        "",
        "## Activities",
        _bullets(plan.activities),
        "",
        "## Assessment",
        _bullets(plan.assessment),
        "",
        "## Evidence",
        _bullets(plan.evidence),
    ]
    if report.warnings:
        lines.extend(["", "## Verification Notes", _bullets(report.warnings)])
    return "\n".join(lines) + "\n"

