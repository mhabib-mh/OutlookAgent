from mcp.server.fastmcp import FastMCP
from services.email.send_email import send_outlook_email
from services.email.fetch_emails import fetch_outlook_emails
from services.email.reply_email import reply_to_outlook_email
from services.email.delete_email import delete_outlook_email
from services.email.forward_email import forward_outlook_email
from services.auth.graph_auth import authenticate_and_get_token
from utils.input_utils import normalize_email_list
import os
from typing import Literal


def create_email_mcp_server():
    mcp_app = FastMCP("outlook-email-mcp-server")

    @mcp_app.tool()
    async def login_tool() -> str:
        """Authenticate with Microsoft Outlook via Device Code Flow"""
        token = authenticate_and_get_token()
        return "✅ Login successful. You can now use Outlook tools."

    @mcp_app.tool()
    async def logout_tool() -> str:
        """Clear saved Outlook access token"""
        token_path = "mcp_server/.token.json"
        if os.path.exists(token_path):
            os.remove(token_path)
            return "🔒 Logout successful. Access token deleted."
        else:
            return "ℹ️ No token was found to delete."

    @mcp_app.tool()
    async def send_email_tool(
        recipient: str,
        subject: str,
        body: str,
        content_type: Literal["Text", "HTML"] = "Text",
        cc: str = "",
        bcc: str = "",
        send_individual: bool = False
    ):
        """
        Enhanced MCP tool to send emails via Microsoft Graph API with advanced recipient management.

        This tool supports sending emails to multiple recipients with flexible options for
        individual or group delivery, CC/BCC support, and both text and HTML content.

        Args:
            recipient (str): Primary recipients as comma or semicolon-separated email addresses.
                           Examples: "user1@example.com, user2@example.com" or "user1@example.com; user2@example.com"
            subject (str): Email subject line.
            body (str): Email content/message body.
            content_type (Literal["Text", "HTML"]): Content format - "Text" for plain text 
                                                   or "HTML" for rich HTML content. Default: "Text"
            cc (str): Optional CC recipients as comma or semicolon-separated email addresses.
                     Examples: "manager@example.com, team@example.com" or "manager@example.com; team@example.com"
            bcc (str): Optional BCC recipients as comma or semicolon-separated email addresses.
                      Examples: "admin@example.com" or "admin1@example.com; admin2@example.com"
            send_individual (bool): Email delivery mode:
                                  - False (default): Send one email to all recipients
                                  - True: Send separate individual emails to each recipient

        Returns:
            dict: Detailed status information with the following structure:
                - status: "complete" if operation finished
                - results: List of delivery results per recipient/group
                  - For group emails: {"recipients": [...], "status": "sent"}
                  - For individual emails: {"recipient": "email", "status": "sent"}
                  - For errors: {"status": "error", "message": "error details"}

        Features:
            ✅ Multiple recipients support (comma or semicolon-separated lists)
            ✅ CC and BCC functionality
            ✅ Individual vs group email delivery options
            ✅ HTML and plain text content support
            ✅ Automatic email validation
            ✅ Comprehensive error handling
            ✅ Detailed delivery status reporting

        Examples:
            # Single recipient with plain text
            send_email_tool(
                recipient="user@example.com",
                subject="Hello",
                body="This is a test message."
            )

            # Multiple recipients with CC/BCC (comma-separated)
            send_email_tool(
                recipient="user1@example.com, user2@example.com",
                subject="Team Update",
                body="Please review the attached information.",
                cc="manager@example.com, team@example.com",
                bcc="admin@example.com"
            )

            # Multiple recipients with semicolon separators
            send_email_tool(
                recipient="user1@example.com; user2@example.com",
                subject="Team Update",
                body="Please review the attached information.",
                cc="manager@example.com; team@example.com"
            )

            # HTML email with individual delivery
            send_email_tool(
                recipient="user1@example.com, user2@example.com",
                subject="Newsletter",
                body="<h1>Welcome!</h1><p>This is an <strong>HTML</strong> email.</p>",
                content_type="HTML",
                send_individual=True
            )

        Error Handling:
            - Invalid email formats are rejected with detailed error messages
            - Network/authentication errors are captured and reported
            - Individual email failures in batch mode are tracked separately

        Note:
            Requires valid Microsoft Graph API authentication. Use login_tool() first
            if you encounter authentication errors.
        """
        to_list = normalize_email_list(recipient)
        cc_list = normalize_email_list(cc)
        bcc_list = normalize_email_list(bcc)

        return await send_outlook_email(
            recipients=to_list,
            subject=subject,
            body=body,
            content_type=content_type,
            cc=cc_list,
            bcc=bcc_list,
            send_individual=send_individual
        )

    @mcp_app.tool()
    async def fetch_email_tool(
        folder: str = "inbox",
        is_read: bool = None,
        sender: str = None,
        email_id: str = None,
        subject: str = None
    ):
        """
        Fetch emails from Outlook.
        
        Args:
            folder: The folder to fetch emails from (default: inbox)
            is_read: Filter by read status (True/False)
            sender: Filter by sender email address
            email_id: Fetch a specific email by ID
            subject: Filter emails containing this text in subject (supports natural language queries)
            
        Returns:
            Email data including IDs for use with reply_email_tool
            
        Examples:
            - fetch_email_tool(subject="meeting notes") - finds emails with "meeting notes" in subject
            - fetch_email_tool(is_read=False) - finds all unread emails
            - fetch_email_tool(email_id="ABC123") - fetches a specific email by ID
        """
        return await fetch_outlook_emails(folder, is_read, sender, email_id, subject)
        
    @mcp_app.tool()
    async def reply_email_tool(email_id: str, reply_message: str):
        """
        Reply to an email using its ID.
        
        Args:
            email_id: The ID of the email to reply to (get this from fetch_email_tool results)
            reply_message: The content of the reply
            
        Returns:
            Status of the reply operation
        
        Example:
            1. First use fetch_email_tool to get emails and their IDs
            2. Then use this tool with the ID of the email you want to reply to
        """
        return await reply_to_outlook_email(email_id, reply_message)
    
    @mcp_app.tool()
    async def delete_email_tool(email_id: str):
        """
        Deletes an email using its ID.
        
        Args:
            email_id: The ID of the email to delete (get this from fetch_email_tool results)            
            
        Returns:
            Status of the delete operation
        
        Example:
            1. First use fetch_email_tool to get emails and their IDs
            2. Then use this tool with the ID of the email you want to delete
        """
        return await delete_outlook_email(email_id)

    @mcp_app.tool()
    async def forward_email_tool(
        email_id: str, 
        to_recipients: str, 
        cc_recipients: str = "", 
        bcc_recipients: str = "", 
        additional_message: str = "", 
        content_type: str = "Text",
        send_individual: bool = False
    ):
        """
        Enhanced MCP tool to forward emails via Microsoft Graph API with advanced recipient management.
        
        This tool supports forwarding emails to multiple recipients with flexible options for
        individual or group delivery, CC/BCC support, and both text and HTML content.
        
        Args:
            email_id (str): The ID of the email to forward (get this from fetch_email_tool results)
            to_recipients (str): Primary recipients as comma or semicolon-separated email addresses.
                               Examples: "user1@example.com, user2@example.com" or "user1@example.com; user2@example.com"
            cc_recipients (str): Optional CC recipients as comma or semicolon-separated email addresses.
                               Examples: "manager@example.com, team@example.com" or "manager@example.com; team@example.com"
            bcc_recipients (str): Optional BCC recipients as comma or semicolon-separated email addresses.
                                Examples: "admin@example.com" or "admin1@example.com; admin2@example.com"
            additional_message (str): Optional additional message to add before the forwarded content
            content_type (str): The content type (Text or HTML, default: Text)
            send_individual (bool): Forward delivery mode:
                                  - False (default): Send one forward to all recipients
                                  - True: Send separate individual forwards to each recipient
            
        Returns:
            dict: Detailed status information with the following structure:
                - status: "complete" if operation finished
                - results: List of forwarding results per recipient/group
                  - For group forwards: {"recipients": [...], "status": "forwarded"}
                  - For individual forwards: {"recipient": "email", "status": "forwarded"}
                  - For errors: {"status": "error", "message": "error details"}
        
        Features:
            ✅ Multiple recipients support (comma or semicolon-separated lists)
            ✅ CC and BCC functionality
            ✅ Individual vs group forward delivery options
            ✅ HTML and plain text content support
            ✅ Automatic email validation
            ✅ Comprehensive error handling
            ✅ Detailed delivery status reporting
        
        Examples:
            # Single recipient forward
            forward_email_tool(
                email_id="ABC123",
                to_recipients="user@example.com",
                additional_message="Please review this email"
            )
            
            # Multiple recipients with CC/BCC (comma-separated)
            forward_email_tool(
                email_id="ABC123",
                to_recipients="user1@example.com, user2@example.com",
                cc_recipients="manager@example.com, team@example.com",
                bcc_recipients="admin@example.com",
                additional_message="Please review this important email"
            )
            
            # Multiple recipients with semicolon separators
            forward_email_tool(
                email_id="ABC123",
                to_recipients="user1@example.com; user2@example.com",
                cc_recipients="manager@example.com; team@example.com"
            )
            
            # Individual forwards to each recipient
            forward_email_tool(
                email_id="ABC123",
                to_recipients="user1@example.com, user2@example.com",
                send_individual=True,
                additional_message="Personal message for you"
            )
        
        Error Handling:
            - Invalid email formats are rejected with detailed error messages
            - Network/authentication errors are captured and reported
            - Individual forward failures in batch mode are tracked separately
        
        Note:
            Requires valid Microsoft Graph API authentication. Use login_tool() first
            if you encounter authentication errors.
        """
        to_list = normalize_email_list(to_recipients)
        cc_list = normalize_email_list(cc_recipients)
        bcc_list = normalize_email_list(bcc_recipients)
        
        return await forward_outlook_email(
            email_id=email_id, 
            to_recipients=to_list, 
            cc_recipients=cc_list, 
            bcc_recipients=bcc_list, 
            additional_message=additional_message, 
            content_type=content_type,
            send_individual=send_individual
        )

    return mcp_app
