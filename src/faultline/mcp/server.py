from mcp.server.fastmcp import FastMCP

from faultline.core.models import Evidence
from faultline.simulator.scenarios import database_pool_exhaustion

mcp = FastMCP("faultline")


@mcp.tool()
def get_incident(incident_id: str) -> dict:
    """Return the incident summary for a known incident scenario."""
    scenario = database_pool_exhaustion()
    if scenario.incident.id != incident_id:
        raise ValueError(f"Unknown incident: {incident_id}")
    return scenario.incident.model_dump(mode="json")


@mcp.tool()
def search_evidence(incident_id: str, source: str | None = None) -> list[dict]:
    """Return evidence associated with an incident, optionally filtered by source."""
    scenario = database_pool_exhaustion()
    if scenario.incident.id != incident_id:
        raise ValueError(f"Unknown incident: {incident_id}")

    evidence: list[Evidence] = scenario.evidence
    if source:
        evidence = [item for item in evidence if item.source == source]
    return [item.model_dump(mode="json") for item in evidence]


if __name__ == "__main__":
    mcp.run()
