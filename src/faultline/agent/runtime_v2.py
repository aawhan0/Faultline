from __future__ import annotations

from faultline.agent.baseline_engine import EvidenceAwareBaselineEngine
from faultline.agent.investigator import DeterministicInvestigator
from faultline.mcp.simulator_provider import SimulatorEvidenceProvider


def run_vertical_slice(incident_id: str):
    """Execute the deterministic investigation-to-diagnosis flow."""
    tools = SimulatorEvidenceProvider()
    investigator = DeterministicInvestigator(tools)
    investigation = investigator.investigate(incident_id)
    incident = tools.get_incident(incident_id)
    diagnosis = EvidenceAwareBaselineEngine().diagnose(incident, investigation.evidence)
    return diagnosis
