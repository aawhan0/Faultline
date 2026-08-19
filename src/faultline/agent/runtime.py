from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from faultline.agent.investigator import DeterministicInvestigator
from faultline.core.models import Diagnosis, Evidence, Incident
from faultline.mcp.client import EvidenceProvider


class DiagnosisEngine(Protocol):
    def diagnose(self, incident: Incident, evidence: list[Evidence]) -> Diagnosis: ...


@dataclass(slots=True)
class AgentRuntime:
    """Coordinates incident investigation behind replaceable interfaces."""

    tools: EvidenceProvider
    diagnosis_engine: DiagnosisEngine

    def investigate(self, incident_id: str) -> Diagnosis:
        investigator = DeterministicInvestigator(self.tools)
        investigation = investigator.investigate(incident_id)
        incident = self.tools.get_incident(investigation.incident_id)
        return self.diagnosis_engine.diagnose(incident, investigation.evidence)
