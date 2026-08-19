from __future__ import annotations

from faultline.core.models import Diagnosis, Incident
from faultline.mcp.client import EvidenceProvider


class EvidenceAwareBaselineEngine:
    """Produces a deterministic diagnosis from retrieved incident evidence.

    This is intentionally a baseline implementation. A model-backed engine can
    replace it later without changing the agent's domain contracts.
    """

    def __init__(self, tools: EvidenceProvider) -> None:
        self._tools = tools

    def diagnose(self, incident: Incident) -> Diagnosis:
        evidence = self._tools.search_evidence(incident.id, "")

        matching = [
            item
            for item in evidence
            if any(
                term in item.content.lower()
                for term in ("pool", "connection", "timeout", "database")
            )
        ]

        if not matching:
            return Diagnosis(
                incident_id=incident.id,
                root_cause="Insufficient evidence to determine root cause.",
                evidence_ids=[],
                confidence=0.0,
                recommended_action="Collect additional logs and metrics before remediation.",
            )

        return Diagnosis(
            incident_id=incident.id,
            root_cause="Database connection pool exhaustion",
            evidence_ids=[item.id for item in matching],
            confidence=0.9,
            recommended_action="Rollback the deployment and verify recovery.",
        )
