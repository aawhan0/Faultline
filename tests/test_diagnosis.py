from faultline.agent.diagnosis import DiagnosisEngine
from faultline.simulator.scenarios import database_pool_exhaustion


def test_diagnosis_identifies_database_pool_exhaustion():
    scenario = database_pool_exhaustion()
    diagnosis = DiagnosisEngine().diagnose(scenario.incident, scenario.evidence)

    assert diagnosis.incident_id == scenario.incident.id
    assert "database connection-pool exhaustion" in diagnosis.root_cause.lower()
    assert diagnosis.evidence_ids
    assert diagnosis.confidence >= 0.8
