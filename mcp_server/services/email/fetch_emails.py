import httpx
from config.settings import GRAPH_API_URL
from services.auth.graph_auth import get_graph_auth_headers

async def fetch_outlook_emails(
    folder: str = "inbox", 
    is_read: bool = None, 
    sender: str = None, 
    email_id: str = None,
    subject: str = None,
    top: int = 10
) -> dict:
   
    headers = get_graph_auth_headers()

    if email_id:
        url = f"{GRAPH_API_URL}/me/messages/{email_id}"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                email_data = response.json()
                return {
                    "status": "success", 
                    "email": email_data,
                    "email_id": email_data.get("id", ""),
                    "subject": email_data.get("subject", ""),
                    "from": email_data.get("from", {}).get("emailAddress", {}).get("address", "")
                }
        except httpx.HTTPStatusError as http_err:
            return {
                "status": "error",
                "message": f"HTTP Error {http_err.response.status_code}: {http_err.response.text}"
            }
        except Exception as e:
            return {"status": "error", "message": f"Error fetching email: {str(e)}"}

    url = f"{GRAPH_API_URL}/me/mailFolders/{folder}/messages"
    query_params = {"$top": top}
    filters = []

    if is_read is not None:
        filters.append(f"isRead eq {str(is_read).lower()}")
    if sender:
        filters.append(f"from/emailAddress/address eq '{sender}'")
    if subject:
        # For subject searches, we'll use a more flexible approach
        # The Microsoft Graph API's contains() is case-sensitive and literal
        # We'll fetch more emails and filter them in code for better results
        top = 50  # Increase the number of emails to fetch when searching by subject

    if filters:
        query_params["$filter"] = " and ".join(filters)

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, params=query_params)
            response.raise_for_status()
            emails = response.json().get("value", [])
            
            # Filter emails by subject if needed (client-side for better matching)
            if subject and not any(f.startswith("contains(subject,") for f in filters):
                # Convert search terms to lowercase for case-insensitive matching
                subject_terms = subject.lower().split()
                filtered_emails = []
                
                for email in emails:
                    email_subject = email.get("subject", "").lower()
                    # Check if all terms in the search query appear in the subject
                    if all(term in email_subject for term in subject_terms):
                        filtered_emails.append(email)
                
                emails = filtered_emails
            
            # Add email_id to each email summary for easier reference
            email_summaries = []
            for email in emails:
                email_summaries.append({
                    "id": email.get("id", ""),
                    "subject": email.get("subject", ""),
                    "from": email.get("from", {}).get("emailAddress", {}).get("address", ""),
                    "received": email.get("receivedDateTime", ""),
                    "is_read": email.get("isRead", False),
                    "preview": email.get("bodyPreview", "")
                })
                
            return {
                "status": "success", 
                "emails": emails,
                "email_summaries": email_summaries
            }
    except httpx.HTTPStatusError as http_err:
        return {
            "status": "error",
            "message": f"HTTP Error {http_err.response.status_code}: {http_err.response.text}"
        }
    except Exception as e:
        return {"status": "error", "message": f"Error fetching emails: {str(e)}"}
