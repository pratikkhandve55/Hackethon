from twilio.rest import Client
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Twilio credentials from .env
account_sid = os.getenv("TWILIO_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_PHONE")

client = Client(account_sid, auth_token)

def send_sms(to_number, message):
    try:
        sms = client.messages.create(
            body=message,
            from_=twilio_number,
            to=to_number
        )
        print(f"[REAL SMS SENT] To: {to_number} | SID: {sms.sid}")
        return {"status": "success", "sid": sms.sid}
    except Exception as e:
        print(f"[SMS ERROR] {e}")
        return {"status": "failed", "error": str(e)}
