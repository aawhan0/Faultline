from __future__ import annotations

from dataclasses import dataclass

from faultline.core.models import Evidence
from faultline.mcp.client import EvidenceProvider


@dataclass(frozen=True, slots=True)
class InvestigationResult:
    incident_id: str
    evidence: list[Evidence]


class DeterministicInvestigator:
    """Collects relevant evidence through the MCP provider boundary."""

    def __init__(self, tools: EvidenceProvider) -> None:
        self._tools = tools

    def investigate(self, incident_id: str) -> InvestigationResult:
        self._tools.get_incident(incident_id)

        queries = ("database", "deployment", "error")
        evidence_by_id: dict[str, Evidence] = {}

        for query in queries:
            for item in self._tools.search_evidence(incident_id, query):
                evidence_by_id[item.id] = item

        return InvestigationResult(
            incident_id=incident_id,
            evidence=list(evidence_by_id.values()),
        )
