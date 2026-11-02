import smtplib
from email.message import EmailMessage

from src.core.config import MAIL_FROM, SMTP_HOST, SMTP_PASSWORD, SMTP_PORT, SMTP_USER


def send_email(to: str, subject: str, body: str) -> None:
    """Send a plain-text email; locally it lands in Mailpit (http://localhost:8025)."""
    message = EmailMessage()
    message["From"] = MAIL_FROM
    message["To"] = to
    message["Subject"] = subject
    message.set_content(body)
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
        # Mailpit needs no login; a real server (e.g. Gmail on port 587) does.
        if SMTP_USER:
            smtp.starttls()
            smtp.login(SMTP_USER, SMTP_PASSWORD)
        smtp.send_message(message)
