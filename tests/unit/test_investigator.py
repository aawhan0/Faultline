from faultline.agent.investigator import DeterministicInvestigator
from faultline.mcp.simulator_provider import SimulatorEvidenceProvider


def test_investigator_collects_relevant_evidence() -> None:
    investigator = DeterministicInvestigator(SimulatorEvidenceProvider())

    result = investigator.investigate("inc-db-pool-001")

    evidence_ids = {item.id for item in result.evidence}

    assert result.incident_id == "inc-db-pool-001"
    assert evidence_ids == {"ev-log-001", "ev-metric-001", "ev-deploy-001"}


def test_investigator_deduplicates_evidence() -> None:
    investigator = DeterministicInvestigator(SimulatorEvidenceProvider())

    result = investigator.investigate("inc-db-pool-001")

    assert len(result.evidence) == len({item.id for item in result.evidence})
