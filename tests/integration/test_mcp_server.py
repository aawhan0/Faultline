import pytest
from mcp.shared.memory import create_connected_server_and_client_session

from faultline.mcp.server import mcp


@pytest.mark.anyio
async def test_mcp_server_exposes_expected_tools() -> None:
    async with create_connected_server_and_client_session(
        mcp._mcp_server
    ) as client:
        await client.initialize()

        result = await client.list_tools()

    tool_names = {tool.name for tool in result.tools}

    assert tool_names == {"get_incident", "search_evidence"}


@pytest.mark.anyio
async def test_get_incident_through_mcp_protocol() -> None:
    async with create_connected_server_and_client_session(
        mcp._mcp_server
    ) as client:
        await client.initialize()

        result = await client.call_tool(
            "get_incident",
            {"incident_id": "INC-0001"},
        )

    assert not result.isError
    assert result.content

    incident_text = result.content[0].text

    assert '"id": "INC-0001"' in incident_text


@pytest.mark.anyio
async def test_search_evidence_through_mcp_protocol() -> None:
    async with create_connected_server_and_client_session(
        mcp._mcp_server
    ) as client:
        await client.initialize()

        result = await client.call_tool(
            "search_evidence",
            {
                "incident_id": "INC-0001",
                "query": "pool",
            },
        )

    assert not result.isError
    assert result.structuredContent is not None

    evidence = result.structuredContent["result"]

    assert evidence
    assert all(
        "pool"
        in f"{item['source']} {item['kind']} {item['content']}".lower()
        for item in evidence
    )


@pytest.mark.anyio
async def test_get_incident_rejects_unknown_incident() -> None:
    async with create_connected_server_and_client_session(
        mcp._mcp_server
    ) as client:
        await client.initialize()

        result = await client.call_tool(
            "get_incident",
            {"incident_id": "UNKNOWN"},
        )

    assert result.isError