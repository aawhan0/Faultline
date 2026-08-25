from faultline.core.models import Diagnosis
from faultline.evals.aggregate import run_evaluations
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


def test_run_evaluations_aggregates_repeated_results() -> None:
    scenario = database_pool_exhaustion()

    result = run_evaluations(
        agent=FakeAgent(),
        scenario=scenario,
        required_evidence_ids={"EV-002", "EV-003"},
        runs=3,
    )

    assert result.total_runs == 3
    assert result.passed_runs == 3
    assert result.pass_rate == 1.0
    assert result.root_cause_accuracy == 1.0
    assert result.evidence_recall == 1.0
    assert result.evidence_precision == 1.0
    assert result.average_confidence == 0.9
    assert len(result.runs) == 3


def test_run_evaluations_rejects_zero_runs() -> None:
    scenario = database_pool_exhaustion()

    try:
        run_evaluations(
            agent=FakeAgent(),
            scenario=scenario,
            required_evidence_ids={"EV-002", "EV-003"},
            runs=0,
        )
    except ValueError as exc:
        assert str(exc) == "runs must be greater than zero."
    else:
        raise AssertionError("Expected ValueError")
