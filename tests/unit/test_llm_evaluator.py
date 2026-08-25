from faultline.core.models import Diagnosis
from faultline.evals.llm import evaluate_diagnosis
from faultline.simulator.scenarios import database_pool_exhaustion


def test_correct_diagnosis_passes_evaluation() -> None:
    scenario = database_pool_exhaustion()

    diagnosis = Diagnosis(
        incident_id=scenario.incident.id,
        root_cause=(
            "Database connection-pool exhaustion caused by "
            "max_overflow being reduced to 0."
        ),
        evidence_ids=["EV-002", "EV-003"],
        confidence=0.95,
        recommended_action=(
            "Restore max_overflow to 20 and verify database "
            "connection pool recovery."
        ),
    )

    result = evaluate_diagnosis(
        scenario,
        diagnosis,
        required_evidence_ids={"EV-002", "EV-003"},
    )

    assert result.root_cause_match is True
    assert result.required_evidence_recall == 1.0
    assert result.evidence_precision == 1.0
    assert result.confidence == 0.95
    assert result.action_present is True
    assert result.passed is True


def test_missing_required_evidence_fails() -> None:
    scenario = database_pool_exhaustion()

    diagnosis = Diagnosis(
        incident_id=scenario.incident.id,
        root_cause=(
            "Database connection-pool exhaustion caused by "
            "max_overflow being reduced to 0."
        ),
        evidence_ids=["EV-002"],
        confidence=0.95,
        recommended_action="Restore max_overflow to 20.",
    )

    result = evaluate_diagnosis(
        scenario,
        diagnosis,
        required_evidence_ids={"EV-002", "EV-003"},
    )

    assert result.required_evidence_recall == 0.5
    assert result.passed is False


def test_unknown_evidence_reduces_precision() -> None:
    scenario = database_pool_exhaustion()

    diagnosis = Diagnosis(
        incident_id=scenario.incident.id,
        root_cause=(
            "Database connection-pool exhaustion caused by "
            "max_overflow being reduced to 0."
        ),
        evidence_ids=["EV-002", "EV-003", "EV-999"],
        confidence=0.95,
        recommended_action="Restore max_overflow to 20.",
    )

    result = evaluate_diagnosis(
        scenario,
        diagnosis,
        required_evidence_ids={"EV-002", "EV-003"},
    )

    assert result.required_evidence_recall == 1.0
    assert result.evidence_precision == 2 / 3
    assert result.passed is False


def test_missing_action_fails() -> None:
    scenario = database_pool_exhaustion()

    diagnosis = Diagnosis(
        incident_id=scenario.incident.id,
        root_cause=(
            "Database connection-pool exhaustion caused by "
            "max_overflow being reduced to 0."
        ),
        evidence_ids=["EV-002", "EV-003"],
        confidence=0.95,
        recommended_action="",
    )

    result = evaluate_diagnosis(
        scenario,
        diagnosis,
        required_evidence_ids={"EV-002", "EV-003"},
    )

    assert result.action_present is False
    assert result.passed is False


def test_invalid_confidence_fails() -> None:
    scenario = database_pool_exhaustion()

    diagnosis = Diagnosis(
        incident_id=scenario.incident.id,
        root_cause=(
            "Database connection-pool exhaustion caused by "
            "max_overflow being reduced to 0."
        ),
        evidence_ids=["EV-002", "EV-003"],
        confidence=1.0,
        recommended_action="Restore max_overflow to 20.",
    )

    result = evaluate_diagnosis(
        scenario,
        diagnosis,
        required_evidence_ids={"EV-002", "EV-003"},
    )

    assert 0.0 <= result.confidence <= 1.0
    assert result.passed is True