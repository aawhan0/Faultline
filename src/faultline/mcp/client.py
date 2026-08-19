from __future__ import annotations

from typing import Protocol

from faultline.core.models import Evidence, Incident


class EvidenceProvider(Protocol):
    """Provider boundary used by the agent to retrieve incident evidence."""

    def get_incident(self, incident_id: str) -> Incident: ...

    def search_evidence(self, incident_id: str, query: str) -> list[Evidence]: ...
