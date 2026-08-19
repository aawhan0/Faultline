from __future__ import annotations

import re

from faultline.core.models import Diagnosis, Evidence, Incident


class DiagnosisEngine:
    """Deterministic baseline used to validate the agent contract before LLM integration."""

    REQUIRED_SIGNALS = (
        "database connection",
        "pool",
        "max_overflow",
        "deployment",
    )

    def diagnose(self, incident: Incident, evidence: list[Evidence]) -> Diagnosis:
        combined = " ".join(item.content.lower() for item in evidence)
        signal_count = sum(signal in combined for signal in self.REQUIRED_SIGNALS)

        if signal_count < 3:
            root_cause = "Insufficient evidence to determine the root cause."
            confidence = 0.2
            supporting = []
            action = "Collect additional logs, metrics, and deployment evidence."
        else:
            supporting = [item.id for item in evidence if item.relevance is not None and item.relevance >= 0.9]
            root_cause = (
                "Database connection-pool exhaustion caused by the latest deployment "
                "reducing database pool overflow capacity."
            )
            confidence = min(0.65 + 0.08 * signal_count, 0.97)
            action = "Investigate deployment 8f31c2 and restore the previous database pool capacity."

        return Diagnosis(
            incident_id=incident.id,
            root_cause=re.sub(r"\s+", " ", root_cause).strip(),
            evidence_ids=supporting,
            confidence=confidence,
            recommended_action=action,
        )
