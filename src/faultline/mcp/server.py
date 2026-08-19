from mcp.server.fastmcp import FastMCP

from faultline.mcp.simulator_provider import SimulatorEvidenceProvider

mcp = FastMCP("faultline")

provider = SimulatorEvidenceProvider()


@mcp.tool()
def get_incident(incident_id: str) -> dict:
    """Return the incident summary for a known incident scenario."""
    incident = provider.get_incident(incident_id)
    return incident.model_dump(mode="json")


@mcp.tool()
def search_evidence(
    incident_id: str,
    query: str = "",
) -> list[dict]:
    """Search evidence associated with an incident."""
    evidence = provider.search_evidence(incident_id, query)
    return [item.model_dump(mode="json") for item in evidence]


if __name__ == "__main__":
    mcp.run()