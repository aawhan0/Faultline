from __future__ import annotations

from dataclasses import dataclass
from faultline.agent.diagnosis import DiagnosisEngine
from faultline.simulator.scenarios import database_pool_exhaustion


@dataclass(frozen=True)
class EvaluationResult:
    passed: bool
    root_cause_match: bool
    evidence_grounded: bool
    confidence: float


def evaluate_baseline() -> EvaluationResult:
    scenario = database_pool_exhaustion()
    diagnosis = DiagnosisEngine().diagnose(scenario.incident, scenario.evidence)

    expected_tokens = {
        "database",
        "pool",
        "deployment",
        "overflow",
    }
    predicted = diagnosis.root_cause.lower()

    root_cause_match = all(token in predicted for token in expected_tokens)
    evidence_grounded = bool(diagnosis.evidence_ids) and all(
        evidence_id in {item.id for item in scenario.evidence}
        for evidence_id in diagnosis.evidence_ids
    )

    return EvaluationResult(
        passed=root_cause_match and evidence_grounded,
        root_cause_match=root_cause_match,
        evidence_grounded=evidence_grounded,
        confidence=diagnosis.confidence,
    )
