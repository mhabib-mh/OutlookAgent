from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Route, Mount

from app.health_check import health_check
from app.sse_handler import handle_sse
from transports.sse_transport import create_sse_transport
from routes.api import routes as api_routes
from server.mcp_email_server import create_email_mcp_server

def create_starlette_app():
    """Creates and configures the Starlette application."""
    sse = create_sse_transport()
    email_mcp_server = create_email_mcp_server()

    app = Starlette(
        debug=True,
        routes=[
            Route("/sse", endpoint=lambda req: handle_sse(req, email_mcp_server, sse)),
            Mount("/messages/", app=sse.handle_post_message),
            Route("/health", endpoint=health_check),
            *api_routes  # API routes for email, calendar, contacts
        ],
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    return app
