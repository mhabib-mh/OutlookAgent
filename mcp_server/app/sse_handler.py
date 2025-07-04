async def handle_sse(request, mcp_server, sse):
    """Handles the SSE connection for MCP server."""
    async with sse.connect_sse(
        request.scope,
        request.receive,
        request._send,  # noqa: SLF001
    ) as (read_stream, write_stream):
        await mcp_server.run(
            read_stream,
            write_stream,
            mcp_server.create_initialization_options(),
        )
