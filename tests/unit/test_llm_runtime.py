from faultline.agent.llm_agent import LLMAgent
from faultline.agent.runtime import AgentRuntime
from faultline.core.models import Evidence, Incident


class FakeEvidenceProvider:
    def get_incident(self, incident_id: str) -> Incident:
        return Incident(
            id=incident_id,
            title="API login failures",
            description="API requests are failing after deployment.",
        )

    def search_evidence(self, incident_id: str, query: str) -> list[Evidence]:
        return [
            Evidence(
                id="EV-001",
                source="logs",
                kind="application_error",
                content="Database connection pool exhausted.",
                relevance=0.99,
            )
        ]


class FakeLLM:
    def generate(self, prompt: str) -> str:
        return """
        {
            "root_cause": "Database connection-pool exhaustion.",
            "evidence_ids": ["EV-001"],
            "confidence": 0.95,
            "recommended_action": "Restore database connection pool capacity."
        }
        """


def test_runtime_can_use_llm_agent() -> None:
    provider = FakeEvidenceProvider()
    agent = LLMAgent(
        tools=provider,
        llm=FakeLLM(),
    )

    runtime = AgentRuntime(
        tools=provider,
        agent=agent,
    )

    diagnosis = runtime.investigate("INC-0001")

    assert diagnosis.incident_id == "INC-0001"
    assert diagnosis.root_cause == "Database connection-pool exhaustion."
    assert diagnosis.evidence_ids == ["EV-001"]