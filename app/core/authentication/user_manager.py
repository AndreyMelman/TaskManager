import logging
from typing import Optional, TYPE_CHECKING, Any

from fastapi_users import BaseUserManager, IntegerIDMixin

from celery_app.celery_app import send_mail
from models import User
from core.config import settings
from core.types.user_id import UserIdType

from templates.email_templates import get_welcome_body, get_welcome_subject

if TYPE_CHECKING:
    from fastapi import Request
    from fastapi import Response

log = logging.getLogger(__name__)


class UserManager(IntegerIDMixin, BaseUserManager[User, UserIdType]):
    reset_password_token_secret = settings.access_token.reset_password_token_secret
    verification_token_secret = settings.access_token.verification_token_secret

    async def on_after_register(
        self,
        user: User,
        request: Optional["Request"] = None,
    ):
        log.info(
            "User %r has registered.",
            user.id,
        )
        subject = get_welcome_subject(user.email)
        body = get_welcome_body(user.email)

        send_mail.delay(user.email, subject, body)


    async def on_after_forgot_password(
        self,
        user: User,
        token: str,
        request: Optional["Request"] = None,
    ):
        log.info(
            "User %r has forgot their password. Reset token: %r",
            user.id,
            token,
        )

    async def on_after_request_verify(
        self,
        user: User,
        token: str,
        request: Optional["Request"] = None,
    ):
        log.info(
            "Verification requested for user %r. Verification token: %r",
            user.id,
            token,
        )

    async def on_after_update(
        self,
        user: User,
        update_dict: dict[str, Any],
        request: Optional["Request"] = None,
    ):
        log.info(
            "User %r has been updated with %r.",
            user.id,
            update_dict,
        )

    async def on_after_login(
        self,
        user: User,
        request: Optional["Request"] = None,
        response: Optional["Response"] = None,
    ):
        log.info(
            "User %r logged in.",
            user.id,
        )

    async def on_before_delete(
        self,
        user: User,
        request: Optional["Request"] = None,
    ):
        log.info(
            "User %r is going to be deleted",
            user.id,
        )
