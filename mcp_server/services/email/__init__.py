"""
Email Services Package
This package provides tools for sending and fetching emails using the Outlook API.

- send_outlook_email: Sends an email via Outlook API.
- fetch_outlook_emails: Fetches emails (read, unread, by sender).
- reply_to_outlook_email: Replies emails (by id).
- delete_outlook_email: Deletes emails (by id).
"""

from .send_email import send_outlook_email
from .fetch_emails import fetch_outlook_emails
from .reply_email import reply_to_outlook_email
from .delete_email import delete_outlook_email

__all__ = ["send_outlook_email", "fetch_outlook_emails", "reply_to_outlook_email", "delete_outlook_email"]

