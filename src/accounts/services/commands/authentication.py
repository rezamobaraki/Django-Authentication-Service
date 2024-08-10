import logging

from django.conf import settings
from redis import Redis

from accounts.models import User
from common.token_generator import generate_otp, generate_token
from core.settings.third_parties.redis_templates import RedisTemplates

logger = logging.getLogger(__name__)


def authentication_register_send_otp(*, cellphone: str):
    otp = generate_otp()
    Redis.set(
        name=RedisTemplates.auth_register_otp.format(cellphone=cellphone),
        value=str(otp),
        ex=settings.REGISTER_OTP_TTL,
    )
    #  send_sms(cellphone=cellphone, otp=otp)
    if settings.DEBUG:
        logger.debug(f"Generated OTP for {cellphone}: {otp}")


def authentication_register_token(*, cellphone: str) -> str:
    token = generate_token()
    Redis.set(
        name=RedisTemplates.format_auth_register_token(token=token),
        value=cellphone,
        ex=settings.REGISTER_TOKEN_TTL,
    )
    return token


def authentication_register_information(*, first_name, last_name, cellphone, email=None):
    token = generate_token()
    data = {"first_name": first_name, "last_name": last_name, "email": email, "cellphone": cellphone, "token": token}
    redis_template = RedisTemplates.format_auth_register_information(token=token)
    Redis.hset(
        name=redis_template,
        mapping=data,
    )
    ttl = settings.REGISTER_TOKEN_TTL
    Redis.expire(name=redis_template, time=ttl)
    return token


def authentication_register_complete(*, token: str, password: str):
    redis_template = RedisTemplates.format_auth_register_information(token=token)
    data = Redis.hgetall(name=redis_template)
    user, _ = User.objects.get_or_create(
        cellphone=data["cellphone"], first_name=data["first_name"], last_name=data["last_name"], email=data["email"]
    )
    user.set_password(password)
    user.save()
    return user


def authentication_login_token(*, cellphone: str) -> str:
    token = generate_token()
    Redis.set(
        name=RedisTemplates.format_auth_login_token(cellphone=cellphone),
        value=token,
        ex=settings.LOGIN_TOKEN_TTL,
    )
    return token
