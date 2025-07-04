from starlette.responses import JSONResponse

async def health_check(request):
    """Health check endpoint."""
    return JSONResponse({"status": "ok", "service": "outlook-mcp-server"})
