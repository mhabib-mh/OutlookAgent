"""
email_utils.py

Utility functions for constructing and formatting email messages
for Microsoft Graph API requests.

Currently includes:
- build_recipients: formats recipient lists
- build_email_payload: constructs full Graph API payload for sending emails
- build_forward_payload: constructs Graph API payload for forwarding emails

If the email logic grows (e.g., support for attachments, inline images,
priority headers, or domain-specific templates), this file can be
split into more granular helpers (e.g., payload_builder.py, recipient_utils.py).
"""

from typing import List, Literal

def build_recipients(addresses: List[str]) -> List[dict]:
    """
    Format a list of email addresses into the structure expected
    by Microsoft Graph API.

    Args:
        addresses (List[str]): List of email addresses.

    Returns:
        List[dict]: Formatted recipient objects.
    """
    return [{"emailAddress": {"address": email}} for email in addresses]

def build_email_payload(
    to: List[str],
    subject: str,
    body: str,
    content_type: Literal["Text", "HTML"],
    cc: List[str],
    bcc: List[str],
) -> dict:
    """
    Construct a Microsoft Graph API email payload.

    Args:
        to (List[str]): Main recipients.
        subject (str): Subject line of the email.
        body (str): Body content.
        content_type (str): 'Text' or 'HTML'.
        cc (List[str]): CC recipients.
        bcc (List[str]): BCC recipients.

    Returns:
        dict: A payload ready to be sent via Graph API.
    """
    return {
        "message": {
            "subject": subject,
            "body": {
                "contentType": content_type,
                "content": body,
            },
            "toRecipients": build_recipients(to),
            "ccRecipients": build_recipients(cc),
            "bccRecipients": build_recipients(bcc),
        },
        "saveToSentItems": "true"
    }

def build_forward_payload(
    to: List[str],
    cc: List[str],
    bcc: List[str],
    additional_message: str = ""
) -> dict:
    """
    Construct a Microsoft Graph API forward email payload.

    Args:
        to (List[str]): Main recipients to forward to.
        cc (List[str]): CC recipients.
        bcc (List[str]): BCC recipients.
        additional_message (str): Optional message to add before forwarded content.

    Returns:
        dict: A payload ready to be sent via Graph API forward endpoint.
    """
    payload = {
        "comment": additional_message,
        "toRecipients": build_recipients(to)
    }
    
    if cc:
        payload["ccRecipients"] = build_recipients(cc)
    
    if bcc:
        payload["bccRecipients"] = build_recipients(bcc)
    
    return payload
