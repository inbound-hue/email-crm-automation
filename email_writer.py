# email_writer.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_email(customer_email: str, appointment_date: str):
    from_email = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")

    subject = "Appointment Confirmation – Horbach Expat Ease"

    body = f"""
Dear Customer,

Nice that I could reach you today, I'm Alex from Horbach Expat Ease.

Here as promised your confirmation for our appointment on {appointment_date}.
Please note it down in your calendar.

You will receive a Teams link shortly before the meeting and we will be talking
about the topics I mentioned.

More details about our services:
https://horbachexpats.com/our-services/

If you have any questions, do not hesitate to reach out.

Warm regards,
Horbach Team
"""

    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = customer_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(from_email, password)
    server.send_message(msg)
    server.quit()

    print(f" Confirmation email sent to {customer_email}")
