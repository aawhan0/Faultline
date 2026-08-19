from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
from pydantic import BaseModel, ConfigDict, Field


class IncidentStatus(StrEnum):
    OPEN = "open"
    INVESTIGATING = "investigating"
    RESOLVED = "resolved"


class Incident(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    title: str
    description: str
    status: IncidentStatus = IncidentStatus.OPEN
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Evidence(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    source: str
    kind: str
    content: str
    timestamp: datetime | None = None
    relevance: float | None = Field(default=None, ge=0.0, le=1.0)


class Diagnosis(BaseModel):
    model_config = ConfigDict(extra="forbid")

    incident_id: str
    root_cause: str
    evidence_ids: list[str]
    confidence: float = Field(ge=0.0, le=1.0)
    recommended_action: str


class IncidentScenario(BaseModel):
    model_config = ConfigDict(extra="forbid")

    incident: Incident
    evidence: list[Evidence]
    expected_root_cause: str
