"""Send order emails through SMTP."""

from __future__ import annotations

import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv

from app.config import BUSINESS

load_dotenv()


class EmailError(Exception):
    pass


def send_order_email(subject: str, body: str, reply_to: str | None = None) -> None:
    host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    port = int(os.getenv("SMTP_PORT", "587"))
    user = os.getenv("SMTP_USER", "")
    password = os.getenv("SMTP_PASSWORD", "")
    to_addr = os.getenv("ORDER_EMAIL_TO", BUSINESS["email"])

    if not user or not password:
        raise EmailError(
            "Email is not configured. Add SMTP_USER and SMTP_PASSWORD to a .env file."
        )

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = f"{BUSINESS['name']} <{user}>"
    message["To"] = to_addr
    if reply_to:
        message["Reply-To"] = reply_to
    message.set_content(body)

    try:
        with smtplib.SMTP(host, port, timeout=20) as smtp:
            smtp.starttls()
            smtp.login(user, password)
            smtp.send_message(message)
    except Exception as exc:
        raise EmailError("We couldn't send your message. Please try again or call us.") from exc
