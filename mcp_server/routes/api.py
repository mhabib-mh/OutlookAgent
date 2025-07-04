from routes.email_api import email_routes
from routes.tools_api import tool_routes

routes = email_routes + tool_routes
