from faultline.agent.runtime import AgentRuntime
from faultline.core.models import Diagnosis, Evidence, Incident


class FakeTools:
    def get_incident(self, incident_id: str) -> Incident:
        return Incident(
            id=incident_id,
            title="Database connection pool exhausted",
            description="Requests are failing after a deployment.",
        )

    def search_evidence(self, incident_id: str, query: str) -> list[Evidence]:
        return [
            Evidence(
                id="ev-001",
                source="application.log",
                kind="log",
                content="database connection pool timeout",
            )
        ]


class FakeDiagnosisEngine:
    def __init__(self) -> None:
        self.received_evidence: list[Evidence] = []

    def diagnose(self, incident: Incident, evidence: list[Evidence]) -> Diagnosis:
        self.received_evidence = evidence
        return Diagnosis(
            incident_id=incident.id,
            root_cause="Database connection pool exhaustion",
            evidence_ids=[item.id for item in evidence],
            confidence=0.9,
            recommended_action="Rollback the deployment and verify recovery.",
        )


def test_agent_runtime_passes_investigation_evidence_to_diagnosis() -> None:
    engine = FakeDiagnosisEngine()
    runtime = AgentRuntime(
        tools=FakeTools(),
        diagnosis_engine=engine,
    )

    diagnosis = runtime.investigate("inc-001")

    assert diagnosis.incident_id == "inc-001"
    assert diagnosis.evidence_ids == ["ev-001"]
    assert [item.id for item in engine.received_evidence] == ["ev-001"]
