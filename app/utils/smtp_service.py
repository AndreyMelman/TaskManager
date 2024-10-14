import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from aiosmtplib import send
from core.config import settings

log = logging.getLogger(__name__)


async def send_email(
    to_email: str,
    subject: str,
    body: str,
):
    message = MIMEMultipart()
    message["From"] = settings.email_a.smtp_user
    message["To"] = to_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    try:
        await send(
            message,
            hostname=settings.email_a.smtp_server,
            port=settings.email_a.smtp_port,
            start_tls=True,
            username=settings.email_a.smtp_user,
            password=settings.email_a.smtp_password,
        )
        log.error("Email sent successfully to %r", to_email)
    except Exception as e:
        log.error("Failed to send email to %r: %r", to_email, e)
