import pytest

from faultline.mcp.simulator_provider import SimulatorEvidenceProvider


def test_provider_returns_known_incident() -> None:
    provider = SimulatorEvidenceProvider()

    incident = provider.get_incident("INC-0001")

    assert incident.id == "INC-0001"
    assert incident.title == "API login failures after deployment"


def test_provider_rejects_unknown_incident() -> None:
    provider = SimulatorEvidenceProvider()

    with pytest.raises(KeyError):
        provider.get_incident("unknown")


def test_provider_filters_evidence_by_query() -> None:
    provider = SimulatorEvidenceProvider()

    evidence = provider.search_evidence("INC-0001", "pool")

    assert evidence
    assert all(
        "pool" in f"{item.source} {item.kind} {item.content}".lower()
        for item in evidence
    )


def test_provider_returns_all_evidence_for_empty_query() -> None:
    provider = SimulatorEvidenceProvider()

    evidence = provider.search_evidence("INC-0001", "")

    assert len(evidence) == 4
