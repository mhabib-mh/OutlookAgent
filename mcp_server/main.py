import os
import sys

# Dynamically set PYTHONPATH based on the environment
if "mcp_server" not in sys.path:
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from services.auth.graph_auth import validate_graph_auth_on_startup
import uvicorn
from app.create_app import create_starlette_app

# Ensure token is available on startup
validate_graph_auth_on_startup()


app = create_starlette_app()

if __name__ == "__main__":
    # print("Starting Outlook MCP server...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
