"""
Microsoft Graph Authentication Module for Outlook MCP Server

This module handles authentication with Microsoft Graph API using the OAuth 2.0 Device Code Flow.
It provides token management, caching, and authentication headers for accessing Outlook services.

Key Features:
- Device Code Flow authentication for secure user consent
- Token caching to avoid repeated authentication
- Automatic token validation on startup
- Graph API headers generation for authenticated requests

Dependencies:
- msal: Microsoft Authentication Library for Python
- config.settings: Application configuration containing client credentials
"""

import os
import sys
import json
import msal
from config import settings

# Path to store the cached access token
TOKEN_CACHE_FILE = "./services/auth/.token.json"

# Initialize Microsoft Authentication Library (MSAL) Public Client Application
# This handles the OAuth 2.0 Device Code Flow for user authentication
app = msal.PublicClientApplication(
    client_id=settings.OUTLOOK_CLIENT_ID,  # Azure AD Application (client) ID
    authority=f"https://login.microsoftonline.com/{settings.OUTLOOK_TENANT_ID}"  # Azure AD tenant authority
)


def load_cached_token() -> str | None:
    """
    Load a previously cached access token from the local file system.
    
    This function checks if a token cache file exists and attempts to load
    the access token from it. This avoids requiring users to re-authenticate
    on every application startup.
    
    Returns:
        str | None: The cached access token if available and valid, None otherwise.
        
    Note:
        The function only checks for the existence of the token, not its validity.
        Token validation happens during API calls.
    """
    if os.path.exists(TOKEN_CACHE_FILE):
        try:
            with open(TOKEN_CACHE_FILE, "r") as f:
                data = json.load(f)
                if "access_token" in data:
                    return data["access_token"]
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Failed to load cached token: {e}")
    return None


def save_token(token_result: dict) -> None:
    """
    Save the access token to a local cache file for future use.
    
    This function stores the access token in a JSON file to enable
    token reuse across application sessions, reducing the need for
    repeated user authentication.
    
    Args:
        token_result (dict): The token response from MSAL containing the access token.
                           Expected to have an 'access_token' key.
                           
    Raises:
        IOError: If unable to create the directory or write the token file.
        
    Security Note:
        The token file should be protected with appropriate file permissions
        in production environments.
    """
    try:
        # Ensure the directory exists before writing the token file
        os.makedirs(os.path.dirname(TOKEN_CACHE_FILE), exist_ok=True)
        
        with open(TOKEN_CACHE_FILE, "w") as f:
            # Only store the access token, not refresh tokens or other sensitive data
            json.dump({"access_token": token_result["access_token"]}, f)
    except (IOError, KeyError) as e:
        print(f"Error: Failed to save token: {e}")
        raise


def authenticate_and_get_token() -> str:
    """
    Perform OAuth 2.0 Device Code Flow authentication with Microsoft Graph.
    
    This function initiates the device code flow, which is ideal for applications
    running on devices without a web browser or with limited input capabilities.
    The user will be prompted to visit a URL and enter a device code to complete
    authentication.
    
    Flow:
    1. Initiate device flow with required scopes
    2. Display authentication instructions to user
    3. Poll for authentication completion
    4. Save and return the access token
    
    Returns:
        str: A valid access token for Microsoft Graph API calls.
        
    Raises:
        ValueError: If the device flow cannot be initiated.
        RuntimeError: If authentication fails or times out.
        
    Example:
        The user will see output like:
        "To sign in, use a web browser to open the page https://microsoft.com/devicelogin
         and enter the code ABC123DEF to authenticate."
    """
    # Initiate the device code flow with the required Microsoft Graph scopes
    flow = app.initiate_device_flow(scopes=settings.OUTLOOK_SCOPES)
    
    if "user_code" not in flow:
        raise ValueError("Failed to start device flow - check client configuration")

    # Display authentication instructions to the user
    print(flow["message"])
    
    # Poll Microsoft's servers until the user completes authentication
    # This is a blocking call that waits for user action
    result = app.acquire_token_by_device_flow(flow)

    if "access_token" in result:
        # Authentication successful - save token for future use
        save_token(result)
        return result["access_token"]
    else:
        # Authentication failed - provide detailed error information
        error_desc = result.get('error_description', 'Unknown authentication error')
        raise RuntimeError(f"Authentication failed: {error_desc}")


def get_token() -> str:
    """
    Get a valid access token, using cached token if available or authenticating if needed.
    
    This is the main entry point for token acquisition. It implements a smart
    caching strategy that first attempts to use a cached token, falling back
    to full authentication only when necessary.
    
    Returns:
        str: A valid access token for Microsoft Graph API calls.
        
    Raises:
        RuntimeError: If authentication fails.
        ValueError: If device flow cannot be initiated.
        
    Note:
        This function does not validate token expiry. If the cached token
        has expired, the first API call will fail with a 401 error, and
        the calling code should handle re-authentication.
    """
    # First, try to use a cached token to avoid unnecessary authentication
    cached = load_cached_token()
    if cached:
        return cached
    
    # No cached token available - perform full authentication
    return authenticate_and_get_token()


def get_graph_auth_headers() -> dict:
    """
    Generate HTTP headers required for authenticated Microsoft Graph API requests.
    
    This function provides the standard headers needed for all Graph API calls,
    including the Bearer token for authentication and appropriate content type.
    
    Returns:
        dict: A dictionary containing the required HTTP headers:
              - Authorization: Bearer token for API authentication
              - Content-Type: JSON content type for request body
              
    Raises:
        RuntimeError: If unable to acquire a valid access token.
        
    Example:
        headers = get_graph_auth_headers()
        response = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers)
    """
    token = get_token()
    if not token:
        raise RuntimeError("Unable to acquire access token for Graph API requests")

    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }


def validate_graph_auth_on_startup() -> None:
    """
    Validate authentication during application startup.
    
    This function ensures that the application can successfully authenticate
    with Microsoft Graph before starting the main server. If authentication
    fails, the application will exit with an error code to prevent running
    in an unusable state.
    
    This is particularly important for server applications that need to
    ensure they have valid credentials before accepting requests.
    
    Raises:
        SystemExit: If authentication fails, the application will exit with code 1.
        
    Side Effects:
        - Prints success/failure messages to stdout
        - May prompt user for authentication if no cached token exists
        - Exits the application on authentication failure
    """
    try:
        token = get_token()
        if not token:
            raise RuntimeError("No token returned from authentication process")
        print("✅ Microsoft Graph authentication successful - server ready")
    except Exception as e:
        print(f"❌ Failed to authenticate with Microsoft Graph: {e}")
        print("Please check your Azure AD configuration and network connectivity")
        sys.exit(1)
