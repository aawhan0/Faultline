from __future__ import annotations

from dataclasses import dataclass

from faultline.agent.runtime import IncidentAgent
from faultline.core.models import Diagnosis, IncidentScenario
from faultline.evals.llm import EvaluationResult, evaluate_diagnosis


@dataclass(frozen=True, slots=True)
class EvaluationRun:
    diagnosis: Diagnosis
    result: EvaluationResult


def run_evaluation(
    agent: IncidentAgent,
    scenario: IncidentScenario,
    required_evidence_ids: set[str],
) -> EvaluationRun:
    """Run an agent against a scenario and evaluate its diagnosis."""

    diagnosis = agent.investigate(scenario.incident.id)

    result = evaluate_diagnosis(
        scenario=scenario,
        diagnosis=diagnosis,
        required_evidence_ids=required_evidence_ids,
    )

    return EvaluationRun(
        diagnosis=diagnosis,
        result=result,
    )