import httpx
from config.settings import GRAPH_API_URL
from services.auth.graph_auth import get_graph_auth_headers

async def reply_to_outlook_email(
    email_id: str,
    reply_message: str,
    content_type: str = "Text"
) -> dict:
    """
    Reply to an email using Microsoft Graph API.
    
    Args:
        email_id: The ID of the email to reply to
        reply_message: The content of the reply
        content_type: The content type (Text or HTML)
        
    Returns:
        A dictionary with status and message
    """

    headers = get_graph_auth_headers()

    reply_data = {
        "message": {
            "body": {
                "contentType": content_type,
                "content": reply_message
            }
        }
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{GRAPH_API_URL}/me/messages/{email_id}/reply",
                json=reply_data,
                headers=headers
            )
            response.raise_for_status()
            return {"status": "success", "message": "Reply sent successfully."}
    except httpx.HTTPStatusError as http_err:
        return {
            "status": "error",
            "message": f"HTTP Error {http_err.response.status_code}: {http_err.response.text}"
        }
    except Exception as e:
        return {"status": "error", "message": f"Error sending reply: {str(e)}"}
