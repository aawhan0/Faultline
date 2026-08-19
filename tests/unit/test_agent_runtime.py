from faultline.agent.runtime import AgentRuntime
from faultline.core.models import Diagnosis, Incident


class FakeTools:
    def get_incident(self, incident_id: str) -> Incident:
        return Incident(
            id=incident_id,
            title="Database connection pool exhausted",
            description="Requests are failing after a deployment.",
        )


class FakeDiagnosisEngine:
    def diagnose(self, incident: Incident) -> Diagnosis:
        return Diagnosis(
            incident_id=incident.id,
            root_cause="Database connection pool exhaustion",
            evidence_ids=["ev-001"],
            confidence=0.9,
            recommended_action="Rollback the deployment and verify recovery.",
        )


def test_agent_runtime_investigates_incident() -> None:
    runtime = AgentRuntime(
        tools=FakeTools(),
        diagnosis_engine=FakeDiagnosisEngine(),
    )

    diagnosis = runtime.investigate("inc-001")

    assert diagnosis.incident_id == "inc-001"
    assert diagnosis.root_cause == "Database connection pool exhaustion"
    assert diagnosis.confidence == 0.9
    assert diagnosis.evidence_ids == ["ev-001"]
