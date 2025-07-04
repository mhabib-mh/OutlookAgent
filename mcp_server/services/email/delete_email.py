import httpx
from config.settings import GRAPH_API_URL
from services.auth.graph_auth import get_graph_auth_headers

async def delete_outlook_email(
    email_id: str
) -> dict:
    """
    Delete an email using Microsoft Graph API.
    
    Args:
        email_id: The ID of the email to delete
                
    Returns:
        A dictionary with status and message
    """

    headers = get_graph_auth_headers()

    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{GRAPH_API_URL}/me/messages/{email_id}",                
                headers=headers
            )
            response.raise_for_status()
            return {"status": "success", "message": "Deleting email was successfull."}
    except httpx.HTTPStatusError as http_err:
        return {
            "status": "error",
            "message": f"HTTP Error {http_err.response.status_code}: {http_err.response.text}"
        }
    except Exception as e:
        return {"status": "error", "message": f"Error deleting email: {str(e)}"}
