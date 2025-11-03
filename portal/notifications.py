import requests
import smtplib
from email.mime.text import MIMEText


def send_whatsapp_message(order):
    whatsapp_api = "https://graph.facebook.com/v18.0/<your_number_id>/messages"
    headers = {"Authorization": f"Bearer <your_access_token>"}
    payload = {
        "messaging_product": "whatsapp",
        "to": "<customer_whatsapp_number>",
        "type": "text",
        "text": {"body": f"Order #{order['id']} has been created!"}
    }
    requests.post(whatsapp_api, headers=headers, json=payload)

def send_email(order):
    msg = MIMEText(f"Order #{order['id']} created successfully!")
    msg['Subject'] = "New Shopify Order"
    msg['From'] = "youremail@gmail.com"
    msg['To'] = "customer@gmail.com"

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login("youremail@gmail.com", "your-app-password")
        server.send_message(msg)
