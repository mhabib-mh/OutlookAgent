from mcp.server.sse import SseServerTransport

def create_sse_transport():
    """Creates an SSE transport instance."""
    return SseServerTransport("/messages/")
