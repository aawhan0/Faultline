from faultline.core.models import Diagnosis
from faultline.evals.runner import run_evaluation
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
            confidence=0.95,
            recommended_action="Restore max_overflow to 20.",
        )


def test_evaluation_runner_returns_diagnosis_and_result() -> None:
    scenario = database_pool_exhaustion()

    run = run_evaluation(
        agent=FakeAgent(),
        scenario=scenario,
        required_evidence_ids={"EV-002", "EV-003"},
    )

    assert run.diagnosis.incident_id == "INC-0001"
    assert run.diagnosis.evidence_ids == ["EV-002", "EV-003"]

    assert run.result.root_cause_match is True
    assert run.result.required_evidence_recall == 1.0
    assert run.result.evidence_precision == 1.0
    assert run.result.passed is True