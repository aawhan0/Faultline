from __future__ import annotations

from dataclasses import dataclass

from faultline.evals.aggregate import AggregateEvaluation


@dataclass(frozen=True, slots=True)
class EvaluationReport:
    """Human-readable representation of aggregate evaluation results."""

    aggregate: AggregateEvaluation
    model: str
    scenario: str

    def to_text(self) -> str:
        return "\n".join(
            [
                "Faultline LLM Evaluation Report",
                "================================",
                f"Model: {self.model}",
                f"Scenario: {self.scenario}",
                f"Total runs: {self.aggregate.total_runs}",
                f"Passed runs: {self.aggregate.passed_runs}",
                f"Pass rate: {self.aggregate.pass_rate:.2%}",
                (
                    f"Root-cause accuracy: "
                    f"{self.aggregate.root_cause_accuracy:.2%}"
                ),
                f"Evidence recall: {self.aggregate.evidence_recall:.2%}",
                (
                    f"Evidence precision: "
                    f"{self.aggregate.evidence_precision:.2%}"
                ),
                (
                    f"Average confidence: "
                    f"{self.aggregate.average_confidence:.2f}"
                ),
            ]
        )
