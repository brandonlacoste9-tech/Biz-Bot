from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import Response
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.models import Booking, Tenant
from datetime import datetime
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/twilio/sms")
async def handle_twilio_sms(request: Request):
    """Handle incoming Twilio SMS webhook"""
    
    try:
        form_data = await request.form()
        from_number = form_data.get("From")
        to_number = form_data.get("To")
        body = form_data.get("Body", "").strip()
        
        logger.info(f"Received SMS from {from_number}: {body}")
        
        # Simple response for now
        response = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>Thank you for contacting us! We'll get back to you soon.</Message>
</Response>"""
        
        return Response(content=response, media_type="application/xml")
        
    except Exception as e:
        logger.error(f"Error processing SMS webhook: {e}")
        raise HTTPException(status_code=500, detail="Error processing webhook")

@router.post("/twilio/whatsapp")
async def handle_twilio_whatsapp(request: Request):
    """Handle incoming Twilio WhatsApp webhook"""
    
    try:
        form_data = await request.form()
        from_number = form_data.get("From")
        to_number = form_data.get("To")
        body = form_data.get("Body", "").strip().lower()
        
        logger.info(f"Received WhatsApp message from {from_number}: {body}")
        
        # Simple booking flow
        response_message = "Bienvenue! / Welcome! Type 'book' to schedule an appointment or 'faq' for frequently asked questions."
        
        if "book" in body or "réserver" in body:
            response_message = "To book an appointment, please visit our website or reply with your preferred date and time."
        elif "faq" in body or "question" in body:
            response_message = "Please visit our FAQ page for common questions, or contact us directly for specific inquiries."
        
        response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{response_message}</Message>
</Response>"""
        
        return Response(content=response, media_type="application/xml")
        
    except Exception as e:
        logger.error(f"Error processing WhatsApp webhook: {e}")
        raise HTTPException(status_code=500, detail="Error processing webhook")
