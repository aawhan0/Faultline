from faultline.agent.diagnosis import DiagnosisEngine
from faultline.agent.runtime import AgentRuntime, DeterministicAgent
from faultline.mcp.simulator_provider import SimulatorEvidenceProvider

EXPECTED_ROOT_CAUSE = "Database connection-pool exhaustion caused by the latest deployment reducing database pool overflow capacity."
INCIDENT_ID = "INC-0001"


def test_database_pool_incident_produces_evidence_backed_diagnosis() -> None:
    tools = SimulatorEvidenceProvider()
    runtime = AgentRuntime(
        tools=tools,
        agent=DeterministicAgent(
            tools=tools,
            diagnosis_engine=DiagnosisEngine(),
        ),
    )

    diagnosis = runtime.investigate(INCIDENT_ID)

    assert diagnosis.incident_id == INCIDENT_ID
    assert diagnosis.root_cause == EXPECTED_ROOT_CAUSE
    assert diagnosis.confidence >= 0.8
    assert set(diagnosis.evidence_ids) == {
        "EV-001",
        "EV-002",
        "EV-003",
        "EV-004",
    }
    assert diagnosis.recommended_action
