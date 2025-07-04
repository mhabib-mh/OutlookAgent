"""
MCP Server Package
This package contains factory methods for creating MCP servers for different services.

- create_email_mcp_server: Email MCP Server
- create_calendar_mcp_server: Calendar MCP Server
- create_contacts_mcp_server: Contacts MCP Server
"""

from .mcp_email_server import create_email_mcp_server

__all__ = [
    "create_email_mcp_server",
]