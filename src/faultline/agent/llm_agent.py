from __future__ import annotations

import json
from dataclasses import dataclass

from faultline.agent.llm import LLMProvider
from faultline.core.models import Diagnosis, Evidence, Incident
from faultline.mcp.client import EvidenceProvider


@dataclass(slots=True)
class LLMAgent:
    """Use an LLM to reason over evidence exposed by the evidence provider."""

    tools: EvidenceProvider
    llm: LLMProvider

    def investigate(self, incident_id: str) -> Diagnosis:
        incident = self.tools.get_incident(incident_id)
        evidence = self.tools.search_evidence(incident_id, "")

        prompt = self._build_prompt(incident, evidence)
        response = self.llm.generate(prompt)

        data = json.loads(response)

        diagnosis = Diagnosis(
            incident_id=incident.id,
            **data,
        )

        known_evidence_ids = {item.id for item in evidence}
        unknown_evidence_ids = set(diagnosis.evidence_ids) - known_evidence_ids

        if unknown_evidence_ids:
            raise ValueError(
                f"Diagnosis references unknown evidence: {sorted(unknown_evidence_ids)}"
            )

        return diagnosis

    @staticmethod
    def _build_prompt(
        incident: Incident,
        evidence: list[Evidence],
    ) -> str:
        evidence_text = "\n".join(
            f"- {item.id} [{item.source}/{item.kind}]: {item.content}"
            for item in evidence
        )

        return (
            "Diagnose the following production incident.\n\n"
            f"Incident: {incident.title}\n"
            f"Description: {incident.description}\n\n"
            "Evidence:\n"
            f"{evidence_text}\n\n"
            "Return JSON with exactly these fields: "
            "root_cause, evidence_ids, confidence, recommended_action."
        )