from faultline.core.models import Diagnosis
from faultline.evals.llm import evaluate_diagnosis
from faultline.simulator.scenarios import database_pool_exhaustion


def test_root_cause_accepts_max_overflow_from_to_wording() -> None:
    scenario = database_pool_exhaustion()

    diagnosis = Diagnosis(
        incident_id=scenario.incident.id,
        root_cause=(
            "The deployment changed the database pool configuration, "
            "reducing max_overflow from 20 to 0."
        ),
        evidence_ids=["EV-002", "EV-003"],
        confidence=0.95,
        recommended_action="Restore max_overflow to 20.",
    )

    result = evaluate_diagnosis(
        scenario,
        diagnosis,
        required_evidence_ids={"EV-002", "EV-003"},
    )

    assert result.root_cause_match is True
    assert result.passed is True


def test_root_cause_accepts_zero_max_overflow_wording() -> None:
    scenario = database_pool_exhaustion()

    diagnosis = Diagnosis(
        incident_id=scenario.incident.id,
        root_cause=(
            "The deployment changed to a zero-max_overflow database "
            "pool configuration, causing connection exhaustion."
        ),
        evidence_ids=["EV-002", "EV-003"],
        confidence=0.95,
        recommended_action="Restore max_overflow to 20.",
    )

    result = evaluate_diagnosis(
        scenario,
        diagnosis,
        required_evidence_ids={"EV-002", "EV-003"},
    )

    assert result.root_cause_match is True
    assert result.passed is True
