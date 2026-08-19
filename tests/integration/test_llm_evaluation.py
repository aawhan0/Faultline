import pytest

from faultline.agent.llm_agent import LLMAgent
from faultline.agent.ollama import OllamaProvider
from faultline.mcp.simulator_provider import SimulatorEvidenceProvider
from faultline.simulator.scenarios import database_pool_exhaustion


@pytest.mark.integration
def test_llm_agent_diagnosis_matches_canonical_scenario() -> None:
    scenario = database_pool_exhaustion()

    agent = LLMAgent(
        tools=SimulatorEvidenceProvider(),
        llm=OllamaProvider(),
    )

    diagnosis = agent.investigate(scenario.incident.id)

    assert diagnosis.incident_id == scenario.incident.id

    assert "database" in diagnosis.root_cause.lower()
    assert "pool" in diagnosis.root_cause.lower()

    assert diagnosis.evidence_ids
    assert "EV-003" in diagnosis.evidence_ids

    assert 0.0 <= diagnosis.confidence <= 1.0

    assert diagnosis.recommended_action