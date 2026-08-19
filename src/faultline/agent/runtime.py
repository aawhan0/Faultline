from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from faultline.core.models import Diagnosis, Incident


class InvestigationTools(Protocol):
    def get_incident(self, incident_id: str) -> Incident: ...


class DiagnosisEngine(Protocol):
    def diagnose(self, incident: Incident) -> Diagnosis: ...


@dataclass(slots=True)
class AgentRuntime:
    """Coordinates incident investigation behind replaceable interfaces."""

    tools: InvestigationTools
    diagnosis_engine: DiagnosisEngine

    def investigate(self, incident_id: str) -> Diagnosis:
        incident = self.tools.get_incident(incident_id)
        return self.diagnosis_engine.diagnose(incident)
