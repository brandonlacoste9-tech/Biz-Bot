from typing import Optional
from twilio.rest import Client
from app.core.config import settings


class TwilioService:
    def __init__(self):
        self.account_sid = settings.TWILIO_ACCOUNT_SID
        self.auth_token = settings.TWILIO_AUTH_TOKEN
        self.whatsapp_number = settings.TWILIO_WHATSAPP_NUMBER
        
        if self.account_sid and self.auth_token:
            self.client = Client(self.account_sid, self.auth_token)
        else:
            self.client = None

    def send_whatsapp_message(self, to: str, message: str) -> Optional[str]:
        """Send WhatsApp message via Twilio"""
        if not self.client:
            print("Twilio client not configured. Skipping WhatsApp message.")
            return None
        
        try:
            message_obj = self.client.messages.create(
                from_=self.whatsapp_number,
                body=message,
                to=f"whatsapp:{to}"
            )
            return message_obj.sid
        except Exception as e:
            print(f"Error sending WhatsApp message: {e}")
            return None

    def send_sms(self, to: str, message: str) -> Optional[str]:
        """Send SMS via Twilio"""
        if not self.client:
            print("Twilio client not configured. Skipping SMS.")
            return None
        
        try:
            message_obj = self.client.messages.create(
                from_=self.whatsapp_number.replace("whatsapp:", ""),
                body=message,
                to=to
            )
            return message_obj.sid
        except Exception as e:
            print(f"Error sending SMS: {e}")
            return None


twilio_service = TwilioService()
