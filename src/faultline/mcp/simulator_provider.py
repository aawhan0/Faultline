from __future__ import annotations

from faultline.core.models import Evidence, Incident
from faultline.mcp.client import EvidenceProvider
from faultline.simulator.scenarios import database_pool_exhaustion


class SimulatorEvidenceProvider(EvidenceProvider):
    """Expose deterministic simulator data through the MCP evidence boundary."""

    def __init__(self) -> None:
        self._scenario = database_pool_exhaustion()

    def get_incident(self, incident_id: str) -> Incident:
        incident = self._scenario.incident
        if incident.id != incident_id:
            raise KeyError(f"Unknown incident: {incident_id}")
        return incident

    def search_evidence(self, incident_id: str, query: str) -> list[Evidence]:
        self.get_incident(incident_id)
        normalized = query.strip().lower()
        if not normalized:
            return list(self._scenario.evidence)

        return [
            item
            for item in self._scenario.evidence
            if normalized in f"{item.source} {item.kind} {item.content}".lower()
        ]
