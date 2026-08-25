from __future__ import annotations

import re
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


def _matches_database_pool_root_cause(root_cause: str) -> bool:
    """Check the causal components of the database-pool scenario."""

    normalized = root_cause.lower()

    database_match = "database" in normalized
    pool_match = "pool" in normalized
    overflow_match = "max_overflow" in normalized

    zero_overflow_match = (
        "zero-max_overflow" in normalized
        or bool(
            re.search(
                r"max_overflow\s*"
                r"(?:"
                r"=\s*0"
                r"|to\s+0"
                r"|from\s+\d+(?:\.\d+)?\s+to\s+0"
                r"|was\s+(?:reduced|set|changed)\s+to\s+0"
                r"|(?:being\s+)?(?:reduced|set|changed)\s+to\s+0"
                r")",
                normalized,
            )
        )
    )

    return (
        database_match
        and pool_match
        and overflow_match
        and zero_overflow_match
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

    root_cause_match = _matches_database_pool_root_cause(
        diagnosis.root_cause
    )

    return EvaluationResult(
        root_cause_match=root_cause_match,
        required_evidence_recall=required_evidence_recall,
        evidence_precision=evidence_precision,
        confidence=diagnosis.confidence,
        action_present=bool(diagnosis.recommended_action.strip()),
    )
