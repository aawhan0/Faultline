from faultline.agent.baseline_engine import EvidenceAwareBaselineEngine
from faultline.agent.runtime import AgentRuntime
from faultline.mcp.simulator_provider import SimulatorEvidenceProvider


EXPECTED_ROOT_CAUSE = "Database connection pool exhaustion"
INCIDENT_ID = "inc-db-pool-001"


def test_database_pool_incident_produces_evidence_backed_diagnosis() -> None:
    tools = SimulatorEvidenceProvider()
    runtime = AgentRuntime(
        tools=tools,
        diagnosis_engine=EvidenceAwareBaselineEngine(),
    )

    diagnosis = runtime.investigate(INCIDENT_ID)

    assert diagnosis.incident_id == INCIDENT_ID
    assert diagnosis.root_cause == EXPECTED_ROOT_CAUSE
    assert diagnosis.confidence >= 0.8
    assert set(diagnosis.evidence_ids) == {
        "ev-log-001",
        "ev-metric-001",
        "ev-deploy-001",
    }
    assert diagnosis.recommended_action
