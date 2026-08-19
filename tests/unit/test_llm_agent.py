import pytest

from faultline.agent.llm import LLMProvider
from faultline.agent.llm_agent import LLMAgent
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
        assert "API login failures" in prompt
        assert "Database connection pool exhausted." in prompt

        return """
        {
            "root_cause": "Database connection-pool exhaustion.",
            "evidence_ids": ["EV-001"],
            "confidence": 0.95,
            "recommended_action": "Restore database connection pool capacity."
        }
        """


def test_llm_agent_produces_diagnosis() -> None:
    provider = FakeEvidenceProvider()
    llm: LLMProvider = FakeLLM()

    agent = LLMAgent(
        tools=provider,
        llm=llm,
    )

    diagnosis = agent.investigate("INC-0001")

    assert diagnosis.incident_id == "INC-0001"
    assert diagnosis.root_cause == "Database connection-pool exhaustion."
    assert diagnosis.evidence_ids == ["EV-001"]
    assert diagnosis.confidence == 0.95
    assert diagnosis.recommended_action == (
        "Restore database connection pool capacity."
    )


class InvalidLLM:
    def generate(self, prompt: str) -> str:
        return "this is not valid JSON"


def test_llm_agent_rejects_invalid_model_output() -> None:
    agent = LLMAgent(
        tools=FakeEvidenceProvider(),
        llm=InvalidLLM(),
    )

    with pytest.raises(ValueError):
        agent.investigate("INC-0001")


class IncompleteLLM:
    def generate(self, prompt: str) -> str:
        return """
        {
            "root_cause": "Database failure"
        }
        """


def test_llm_agent_rejects_incomplete_model_output() -> None:
    agent = LLMAgent(
        tools=FakeEvidenceProvider(),
        llm=IncompleteLLM(),
    )

    with pytest.raises(ValueError):
        agent.investigate("INC-0001")


class UngroundedLLM:
    def generate(self, prompt: str) -> str:
        return """
        {
            "root_cause": "Database connection-pool exhaustion.",
            "evidence_ids": ["EV-999"],
            "confidence": 0.95,
            "recommended_action": "Restore database connection pool capacity."
        }
        """


def test_llm_agent_rejects_ungrounded_evidence() -> None:
    agent = LLMAgent(
        tools=FakeEvidenceProvider(),
        llm=UngroundedLLM(),
    )

    with pytest.raises(ValueError, match="unknown evidence"):
        agent.investigate("INC-0001")