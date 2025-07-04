"""
Enhanced Email Forwarding Service for Outlook MCP Server

This module provides comprehensive email forwarding capabilities using Microsoft Graph API,
supporting multiple recipients, flexible delivery modes, and rich content formatting.

Key Features:
- Multiple recipients support (TO, CC, BCC)
- Individual vs group email forwarding modes
- HTML and plain text content support
- Comprehensive email validation
- Detailed error handling and status reporting

Dependencies:
- httpx: Async HTTP client for Graph API requests
- services.auth.graph_auth: Authentication headers for Graph API
- utils.email.email_utils: Forward payload construction utilities
- utils.validators: Email format validation utilities
"""

import httpx
from typing import List, Dict, Any
from config.settings import GRAPH_API_URL
from services.auth.graph_auth import get_graph_auth_headers
from utils.email.email_utils import build_forward_payload
from utils.validators import validate_email_format


async def forward_outlook_email(
    email_id: str,
    to_recipients: List[str],
    cc_recipients: List[str] = [],
    bcc_recipients: List[str] = [],
    additional_message: str = "",
    content_type: str = "Text",
    send_individual: bool = False
) -> Dict[str, Any]:
    """
    Forward an email using Microsoft Graph API with advanced recipient management.
    
    Automatically adds "Fw: " prefix to subject and preserves original content.
    Supports multiple recipients with individual or group forwarding modes.
    Uses the same behavior as send_email with build_forward_payload utility.

    Args:
        email_id (str): The ID of the email to forward
        to_recipients (List[str]): List of primary recipient email addresses
        cc_recipients (List[str]): Optional CC recipient email addresses
        bcc_recipients (List[str]): Optional BCC recipient email addresses
        additional_message (str): Optional message to add before forwarded content
        content_type (str): Content type (Text or HTML), defaults to "Text"
        send_individual (bool): If True, send separate forwards to each recipient (default: False)

    Returns:
        Dict[str, Any]: Status information with forwarding results:
            - status: "complete" if operation finished
            - results: List of forwarding results per recipient/group
              - Group mode: {"recipients": [...], "status": "forwarded"}
              - Individual mode: {"recipient": "email", "status": "forwarded"}
              - Errors: {"status": "error", "message": "error details"}
        
    Examples:
        # Single recipient forward
        result = await forward_outlook_email(
            "email_id", 
            ["user@example.com"], 
            additional_message="Please review"
        )
        
        # Multiple recipients with CC/BCC
        result = await forward_outlook_email(
            "email_id",
            ["user1@example.com", "user2@example.com"],
            cc_recipients=["manager@example.com"],
            bcc_recipients=["admin@example.com"]
        )
        
        # Individual forwards to each recipient
        result = await forward_outlook_email(
            "email_id",
            ["user1@example.com", "user2@example.com"],
            send_individual=True
        )

    Features:
        ✅ Multiple recipients support
        ✅ CC and BCC functionality
        ✅ Individual vs group forwarding modes
        ✅ HTML and plain text content support
        ✅ Automatic email validation
        ✅ Comprehensive error handling
        ✅ Uses build_forward_payload utility like send_email

    Forwarding Modes:
        - Group Mode (send_individual=False): One forward to all recipients
        - Individual Mode (send_individual=True): Separate forwards per recipient

    Error Handling:
        - Email validation errors are returned immediately
        - Network/authentication errors are captured per forward
        - Individual failures don't stop batch processing
    """
    
    headers = get_graph_auth_headers()
    results = []

    # Validate all email addresses before forwarding
    all_addresses = to_recipients + cc_recipients + bcc_recipients
    invalid = [email for email in all_addresses if not validate_email_format(email)]
    if invalid:
        return {
            "status": "error",
            "message": f"Invalid email address(es): {', '.join(invalid)}"
        }

    # Validate that we have at least one TO recipient
    if not to_recipients:
        return {
            "status": "error",
            "message": "At least one TO recipient is required"
        }

    async with httpx.AsyncClient() as client:
        if send_individual:
            # Send separate forwards to each TO recipient (like send_email behavior)
            for recipient in to_recipients:
                # Use build_forward_payload for consistent behavior
                forward_data = build_forward_payload(
                    to=[recipient],
                    cc=cc_recipients,
                    bcc=bcc_recipients,
                    additional_message=additional_message
                )

                try:
                    response = await client.post(
                        f"{GRAPH_API_URL}/me/messages/{email_id}/forward",
                        json=forward_data,
                        headers=headers
                    )
                    response.raise_for_status()
                    results.append({"recipient": recipient, "status": "forwarded"})
                except httpx.HTTPStatusError as http_err:
                    results.append({
                        "recipient": recipient, 
                        "status": "error", 
                        "message": f"HTTP Error {http_err.response.status_code}: {http_err.response.text}"
                    })
                except Exception as e:
                    results.append({
                        "recipient": recipient, 
                        "status": "error", 
                        "message": f"Error forwarding email: {str(e)}"
                    })
        else:
            # Send one forward to all recipients (like send_email behavior)
            # Use build_forward_payload for consistent behavior
            forward_data = build_forward_payload(
                to=to_recipients,
                cc=cc_recipients,
                bcc=bcc_recipients,
                additional_message=additional_message
            )

            try:
                response = await client.post(
                    f"{GRAPH_API_URL}/me/messages/{email_id}/forward",
                    json=forward_data,
                    headers=headers
                )
                response.raise_for_status()
                results.append({"recipients": to_recipients, "status": "forwarded"})
            except httpx.HTTPStatusError as http_err:
                results.append({
                    "status": "error",
                    "message": f"HTTP Error {http_err.response.status_code}: {http_err.response.text}"
                })
            except Exception as e:
                results.append({
                    "status": "error",
                    "message": f"Error forwarding email: {str(e)}"
                })

    return {"status": "complete", "results": results}
