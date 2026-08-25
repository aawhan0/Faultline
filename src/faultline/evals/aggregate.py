from __future__ import annotations

from dataclasses import dataclass

from faultline.agent.runtime import IncidentAgent
from faultline.core.models import IncidentScenario
from faultline.evals.runner import EvaluationRun, run_evaluation


@dataclass(frozen=True, slots=True)
class AggregateEvaluation:
    runs: list[EvaluationRun]
    total_runs: int
    passed_runs: int
    pass_rate: float
    root_cause_accuracy: float
    evidence_recall: float
    evidence_precision: float
    average_confidence: float


def run_evaluations(
    agent: IncidentAgent,
    scenario: IncidentScenario,
    required_evidence_ids: set[str],
    runs: int,
) -> AggregateEvaluation:
    """Run repeated evaluations and aggregate their metrics."""

    if runs <= 0:
        raise ValueError("runs must be greater than zero.")

    results = [
        run_evaluation(
            agent=agent,
            scenario=scenario,
            required_evidence_ids=required_evidence_ids,
        )
        for _ in range(runs)
    ]

    evaluations = [run.result for run in results]

    passed_runs = sum(result.passed for result in evaluations)

    return AggregateEvaluation(
        runs=results,
        total_runs=len(results),
        passed_runs=passed_runs,
        pass_rate=passed_runs / len(results),
        root_cause_accuracy=sum(
            result.root_cause_match for result in evaluations
        ) / len(results),
        evidence_recall=sum(
            result.required_evidence_recall for result in evaluations
        ) / len(results),
        evidence_precision=sum(
            result.evidence_precision for result in evaluations
        ) / len(results),
        average_confidence=sum(
            result.confidence for result in evaluations
        ) / len(results),
    )
