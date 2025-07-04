from starlette.routing import Route
from starlette.responses import JSONResponse
from starlette.requests import Request
from services.email.send_email import send_outlook_email
from services.email.fetch_emails import fetch_outlook_emails
from services.email.reply_email import reply_to_outlook_email
from services.email.delete_email import delete_outlook_email
from services.email.forward_email import forward_outlook_email

from starlette.requests import Request
from starlette.responses import JSONResponse
from services.email.send_email import send_outlook_email
from utils import normalize_email_list, validate_email_format

async def send_email_route(request: Request):
    try:
        data = await request.json()

        recipient = data.get("recipient")
        subject = data.get("subject")
        body = data.get("body") or data.get("message") or "No content provided."
        content_type = data.get("content_type", "Text")
        cc = data.get("cc", [])
        bcc = data.get("bcc", [])
        send_individual = data.get("send_individual", False)

        if not recipient or not subject:
            return JSONResponse({"error": "Missing required fields: 'recipient' and 'subject'"}, status_code=400)

        # Normalize all address fields
        to_list = normalize_email_list(recipient)
        cc_list = normalize_email_list(cc)
        bcc_list = normalize_email_list(bcc)

        # Validate all email addresses
        all_emails = to_list + cc_list + bcc_list
        invalid = [email for email in all_emails if not validate_email_format(email)]
        if invalid:
            return JSONResponse({"error": f"Invalid email address(es): {', '.join(invalid)}"}, status_code=400)

        result = await send_outlook_email(
            recipients=to_list,
            subject=subject,
            body=body,
            content_type=content_type,
            cc=cc_list,
            bcc=bcc_list,
            send_individual=send_individual
        )

        return JSONResponse(result)

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


async def fetch_emails_route(request: Request):
    try:
        data = request.query_params
        folder = data.get("folder", "inbox")
        is_read = data.get("is_read") == "true" if "is_read" in data else None
        sender = data.get("sender")
        email_id = data.get("email_id")
        subject = data.get("subject")
        result = await fetch_outlook_emails(folder, is_read, sender, email_id, subject)
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

async def reply_email_route(request: Request):
    try:
        data = await request.json()
        email_id = data.get("email_id")
        reply_message = data.get("reply_message")
        
        if not email_id or not reply_message:
            return JSONResponse({"error": "Missing required fields: email_id and reply_message"}, status_code=400)
            
        result = await reply_to_outlook_email(email_id, reply_message)
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
async def delete_email_route(request: Request):
    try:
        data = await request.json()
        email_id = data.get("email_id")   
        
        if not email_id:
            return JSONResponse({"error": "Missing required field: email_id"}, status_code=400)
            
        result = await delete_outlook_email(email_id)
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
async def forward_email_route(request: Request):
    try:
        data = await request.json()
        email_id = data.get("email_id")
        to_recipient = data.get("recipient")
        cc_recipient = data.get("cc", [])
        bcc_recipient = data.get("bcc", [])
        additional_message = data.get("additional_message", "")
        content_type = data.get("content_type", "Text")
        send_individual = data.get("send_individual", False)

        
        if not email_id or not to_recipient:
            return JSONResponse({"error": "Missing required fields: email_id and recipient"}, status_code=400)
            
        # Normalize all address fields
        to_list = normalize_email_list(to_recipient)
        cc_list = normalize_email_list(cc_recipient)
        bcc_list = normalize_email_list(bcc_recipient)

        # Validate all email addresses
        all_emails = to_list + cc_list + bcc_list
        invalid = [email for email in all_emails if not validate_email_format(email)]
        if invalid:
            return JSONResponse({"error": f"Invalid email address(es): {', '.join(invalid)}"}, status_code=400)
    
        result = await forward_outlook_email(
            email_id=email_id, 
            to_recipients=to_list, 
            cc_recipients=cc_list, 
            bcc_recipients=bcc_list, 
            additional_message=additional_message, 
            content_type=content_type,
            send_individual=send_individual
        )
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

email_routes = [
    Route("/api/send-email", send_email_route, methods=["POST"]),
    Route("/api/fetch-emails", fetch_emails_route, methods=["GET"]),
    Route("/api/reply-email", reply_email_route, methods=["POST"]),
    Route("/api/delete-email", delete_email_route, methods=["DELETE"]),
    Route("/api/forward-email", forward_email_route, methods=["POST"]),
]
