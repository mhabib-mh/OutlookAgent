"""
Enhanced Email Sending Service for Outlook MCP Server

This module provides comprehensive email sending capabilities using Microsoft Graph API,
supporting multiple recipients, flexible delivery modes, and rich content formatting.

Key Features:
- Multiple recipients support (TO, CC, BCC)
- Individual vs group email delivery modes
- HTML and plain text content support
- Comprehensive email validation
- Detailed error handling and status reporting

Dependencies:
- httpx: Async HTTP client for Graph API requests
- services.auth.graph_auth: Authentication headers for Graph API
- utils.email.email_utils: Email payload construction utilities
- utils.validators: Email format validation utilities
"""

import httpx
from typing import List, Literal, Dict, Any
from config.settings import GRAPH_API_URL
from services.auth.graph_auth import get_graph_auth_headers
from utils.email.email_utils import build_email_payload
from utils.validators import validate_email_format


async def send_outlook_email(
    recipients: List[str],
    subject: str,
    body: str,
    content_type: Literal["Text", "HTML"] = "Text",
    send_individual: bool = False,
    cc: List[str] = [],
    bcc: List[str] = [],
) -> Dict[str, Any]:
    """
    Send one or more emails via Microsoft Graph API with advanced recipient management.

    Args:
        recipients (List[str]): List of primary recipient email addresses.
        subject (str): Email subject line.
        body (str): Email content/message body.
        content_type (Literal["Text", "HTML"]): Content format - "Text" or "HTML" (default: "Text").
        send_individual (bool): If True, send separate emails to each recipient (default: False).
        cc (List[str]): Optional CC recipients.
        bcc (List[str]): Optional BCC recipients.

    Returns:
        Dict[str, Any]: Status information with delivery results:
            - status: "complete" if operation finished
            - results: List of delivery results per recipient/group
              - Group mode: {"recipients": [...], "status": "sent"}
              - Individual mode: {"recipient": "email", "status": "sent"}
              - Errors: {"status": "error", "message": "error details"}

    Features:
        ✅ Multiple recipients support
        ✅ CC and BCC functionality
        ✅ Individual vs group delivery modes
        ✅ HTML and plain text content support
        ✅ Automatic email validation
        ✅ Comprehensive error handling

    Examples:
        # Single recipient
        await send_outlook_email(
            recipients=["user@example.com"],
            subject="Hello",
            body="This is a test message."
        )

        # Multiple recipients with CC/BCC
        await send_outlook_email(
            recipients=["user1@example.com", "user2@example.com"],
            subject="Team Update",
            body="Please review the information.",
            cc=["manager@example.com"],
            bcc=["admin@example.com"]
        )

        # HTML email with individual delivery
        await send_outlook_email(
            recipients=["user1@example.com", "user2@example.com"],
            subject="Newsletter",
            body="<h1>Welcome!</h1><p>HTML content here</p>",
            content_type="HTML",
            send_individual=True
        )

    Delivery Modes:
        - Group Mode (send_individual=False): One email to all recipients
        - Individual Mode (send_individual=True): Separate emails per recipient

    Error Handling:
        - Email validation errors are returned immediately
        - Network/authentication errors are captured per email
        - Individual failures don't stop batch processing
    """
    # Get authentication headers for Microsoft Graph API
    headers = get_graph_auth_headers()
    results = []

    # Validate all email addresses before sending
    all_addresses = recipients + cc + bcc
    invalid = [email for email in all_addresses if not validate_email_format(email)]
    if invalid:
        return {
            "status": "error",
            "message": f"Invalid email address(es): {', '.join(invalid)}"
        }

    async with httpx.AsyncClient() as client:
        if send_individual:
            # Send separate emails to each recipient
            for recipient in recipients:
                payload = build_email_payload(
                    to=[recipient],
                    subject=subject,
                    body=body,
                    content_type=content_type,
                    cc=cc,
                    bcc=bcc
                )
                try:
                    response = await client.post(
                        f"{GRAPH_API_URL}/me/sendMail",
                        json=payload,
                        headers=headers
                    )
                    response.raise_for_status()
                    results.append({"recipient": recipient, "status": "sent"})
                except Exception as e:
                    results.append({"recipient": recipient, "status": "error", "message": str(e)})
        else:
            # Send one email to all recipients
            payload = build_email_payload(
                to=recipients,
                subject=subject,
                body=body,
                content_type=content_type,
                cc=cc,
                bcc=bcc
            )
            try:
                response = await client.post(
                    f"{GRAPH_API_URL}/me/sendMail",
                    json=payload,
                    headers=headers
                )
                response.raise_for_status()
                results.append({"recipients": recipients, "status": "sent"})
            except Exception as e:
                results.append({"status": "error", "message": str(e)})

    return {"status": "complete", "results": results}
