from __future__ import annotations

from dataclasses import dataclass

from faultline.core.models import Diagnosis, IncidentScenario


@dataclass(frozen=True, slots=True)
class EvaluationResult:
    root_cause_match: bool
    required_evidence_recall: float
    evidence_precision: float
    confidence: float
    action_present: bool

    @property
    def passed(self) -> bool:
        return (
            self.root_cause_match
            and self.required_evidence_recall == 1.0
            and self.evidence_precision == 1.0
            and self.action_present
            and 0.0 <= self.confidence <= 1.0
        )


def evaluate_diagnosis(
    scenario: IncidentScenario,
    diagnosis: Diagnosis,
    required_evidence_ids: set[str],
) -> EvaluationResult:
    """Evaluate an LLM diagnosis against deterministic scenario ground truth."""

    actual_evidence_ids = set(diagnosis.evidence_ids)
    available_evidence_ids = {item.id for item in scenario.evidence}

    if required_evidence_ids:
        required_evidence_recall = len(
            required_evidence_ids & actual_evidence_ids
        ) / len(required_evidence_ids)
    else:
        required_evidence_recall = 1.0

    if actual_evidence_ids:
        evidence_precision = len(
            actual_evidence_ids & available_evidence_ids
        ) / len(actual_evidence_ids)
    else:
        evidence_precision = 0.0

    root_cause = diagnosis.root_cause.lower()

    root_cause_match = (
        "database" in root_cause
        and "pool" in root_cause
        and "max_overflow" in root_cause
        and "0" in root_cause
    )

    return EvaluationResult(
        root_cause_match=root_cause_match,
        required_evidence_recall=required_evidence_recall,
        evidence_precision=evidence_precision,
        confidence=diagnosis.confidence,
        action_present=bool(diagnosis.recommended_action.strip()),
    )