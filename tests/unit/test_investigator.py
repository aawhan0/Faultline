from faultline.agent.investigator import DeterministicInvestigator
from faultline.mcp.simulator_provider import SimulatorEvidenceProvider


def test_investigator_collects_relevant_evidence() -> None:
    investigator = DeterministicInvestigator(SimulatorEvidenceProvider())

    result = investigator.investigate("INC-0001")

    evidence_ids = {item.id for item in result.evidence}

    assert result.incident_id == "INC-0001"
    assert evidence_ids == {
        "EV-001",
        "EV-002",
        "EV-003",
        "EV-004",
    }


def test_investigator_deduplicates_evidence() -> None:
    investigator = DeterministicInvestigator(SimulatorEvidenceProvider())

    result = investigator.investigate("INC-0001")

    assert len(result.evidence) == len({item.id for item in result.evidence})
