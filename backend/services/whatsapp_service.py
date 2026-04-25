import os
import requests

ULTRAMSG_INSTANCE = os.environ.get("ULTRAMSG_INSTANCE_ID", "")
ULTRAMSG_TOKEN = os.environ.get("ULTRAMSG_TOKEN", "")

def send_hot_lead_whatsapp(name, phone, property_type, location_preference, budget):
    """
    Triggers a WhatsApp message using UltraMsg for Hot leads.
    """
    if not ULTRAMSG_INSTANCE or not ULTRAMSG_TOKEN:
        print("UltraMsg not configured for hot lead notification.")
        return False
        
    if not phone:
        print("No phone number provided for hot lead.")
        return False

    try:
        clean_phone = phone.replace("whatsapp:", "").strip()
        # Add +91 if not present and starts with 10 digits
        if not clean_phone.startswith("+"):
            clean_phone = "+91" + clean_phone.lstrip("0")
            
        msg = (
            f"🌟 *Madhavi Enterprises - Priority Update* 🌟\n\n"
            f"Hello {name or 'Valued Customer'},\n\n"
            f"Thank you for your high interest! Our AI noted your requirements:\n"
            f"*Property Type:* {property_type or 'Not specified'}\n"
            f"*Location:* {location_preference or 'Not specified'}\n"
            f"*Budget:* {budget or 'Not specified'}\n\n"
            f"A senior property expert will contact you shortly.\n\n"
            f"For immediate assistance, please reply to this message or call us at +91 98765 43210.\n"
            f"Web: www.madhavienterprise.com"
        )
        url = f"https://api.ultramsg.com/{ULTRAMSG_INSTANCE}/messages/chat"
        res = requests.post(url, json={"token": ULTRAMSG_TOKEN, "to": clean_phone, "body": msg}, timeout=10)
        
        sent = res.status_code == 200
        print(f"Hot lead WhatsApp sent to {clean_phone}: {sent}")
        return sent
    except Exception as e:
        print(f"Hot lead WhatsApp error: {e}")
        return False
