from faultline.core.models import Diagnosis
from faultline.evals.aggregate import run_evaluations
from faultline.evals.report import EvaluationReport
from faultline.simulator.scenarios import database_pool_exhaustion


class FakeAgent:
    def investigate(self, incident_id: str) -> Diagnosis:
        return Diagnosis(
            incident_id=incident_id,
            root_cause=(
                "Database connection-pool exhaustion caused by "
                "max_overflow being reduced to 0."
            ),
            evidence_ids=["EV-002", "EV-003"],
            confidence=0.9,
            recommended_action="Restore max_overflow to 20.",
        )


def test_evaluation_report_formats_aggregate_results() -> None:
    scenario = database_pool_exhaustion()

    aggregate = run_evaluations(
        agent=FakeAgent(),
        scenario=scenario,
        required_evidence_ids={"EV-002", "EV-003"},
        runs=2,
    )

    report = EvaluationReport(
        aggregate=aggregate,
        model="test-model",
        scenario="database_pool_exhaustion",
    )

    text = report.to_text()

    assert "Faultline LLM Evaluation Report" in text
    assert "Model: test-model" in text
    assert "Scenario: database_pool_exhaustion" in text
    assert "Total runs: 2" in text
    assert "Passed runs: 2" in text
    assert "Pass rate: 100.00%" in text
    assert "Root-cause accuracy: 100.00%" in text
    assert "Evidence recall: 100.00%" in text
    assert "Evidence precision: 100.00%" in text
    assert "Average confidence: 0.90" in text
