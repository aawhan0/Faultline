import pytest

from faultline.agent.llm_agent import LLMAgent
from faultline.agent.ollama import OllamaProvider
from faultline.mcp.simulator_provider import SimulatorEvidenceProvider


@pytest.mark.integration
def test_llm_agent_diagnoses_canonical_incident() -> None:
    agent = LLMAgent(
        tools=SimulatorEvidenceProvider(),
        llm=OllamaProvider(),
    )

    diagnosis = agent.investigate("INC-0001")

    assert diagnosis.incident_id == "INC-0001"
    assert diagnosis.root_cause
    assert diagnosis.evidence_ids
    assert diagnosis.confidence >= 0.0
    assert diagnosis.recommended_action