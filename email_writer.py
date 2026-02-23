import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_email(customer_email: str, appointment_date: str | None):
    from_email = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")

    subject = "Appointment Confirmation – Horbach Expat Ease"

    if appointment_date:
        body = f"""
Dear Customer,

Nice that I could reach you today.

Here as promised your confirmation for our appointment on {appointment_date}.

Warm regards,
Horbach Team
"""
    else:
        body = """
Dear Customer,

Thank you for your submission. We have received your audio.

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

    print(f"Confirmation email sent to {customer_email}")
