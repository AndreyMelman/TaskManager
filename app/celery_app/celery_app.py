import smtplib
import logging

from core.config import settings

from celery import Celery

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

log = logging.getLogger(__name__)

celery_app = Celery(
    "notification",
    broker=str(settings.celery.celery_broker_url),
    backend=str(settings.celery.celery_result_backend),
)

celery_app.conf.update(
    broker_connection_retry_on_startup=True,
)


@celery_app.task
def send_mail(
    to_email: str,
    subject: str,
    body: str,
):
    message = MIMEMultipart()
    message["From"] = settings.email_a.smtp_user
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP(
            settings.email_a.smtp_server, settings.email_a.smtp_port
        ) as server:
            server.starttls()
            server.login(settings.email_a.smtp_user, settings.email_a.smtp_password)
            server.sendmail(settings.email_a.smtp_user, to_email, message.as_string())

    except Exception as e:
        log.error("Failed to send email to %r: %r", to_email, e)
