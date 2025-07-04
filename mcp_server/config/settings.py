import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Microsoft Graph API
GRAPH_API_URL = os.getenv("GRAPH_API_URL", "https://graph.microsoft.com/v1.0")
OUTLOOK_CLIENT_ID = os.getenv("OUTLOOK_CLIENT_ID")
OUTLOOK_TENANT_ID = os.getenv("OUTLOOK_TENANT_ID")
OUTLOOK_SCOPES = os.getenv("OUTLOOK_SCOPES").split()

# Server Configuration
PORT = int(os.getenv("PORT", 8000))
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
