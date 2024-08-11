from django.conf import settings

from accounts.models import User
from accounts.tasks import send_sms_task
from common.token_generator import generate_otp, generate_token
from core.settings.third_parties.redis import Redis
from core.settings.third_parties.redis_templates import RedisKeyTemplates


def send_registration_otp(cellphone: str):
    otp = generate_otp()
    Redis.set(
        name=RedisKeyTemplates.format_register_otp_key(cellphone=cellphone),
        value=str(otp),
        ex=settings.REGISTER_OTP_TTL,
    )
    # SMS sending
    send_sms_task.delay(cellphone=cellphone, message=f"Your OTP is {otp}")


def generate_registration_token(cellphone: str) -> str:
    token = generate_token()
    data = {"cellphone": cellphone, "token": token}
    redis_template = RedisKeyTemplates.format_register_token_key(token=token)
    ttl = settings.REGISTER_TOKEN_TTL
    Redis.hset(
        name=redis_template,
        mapping=data,
    )
    Redis.expire(name=redis_template, time=ttl)
    return token


def store_registration_information(*, token, first_name, last_name, email):
    redis_template = RedisKeyTemplates.format_register_token_key(token=token)
    existing_data = Redis.hgetall(redis_template)
    information = {"first_name": first_name, "last_name": last_name, "email": email}
    existing_data.update(information)
    Redis.hset(name=redis_template, mapping=existing_data)
    return token


def complete_registration(token: str, password: str):
    redis_template = RedisKeyTemplates.format_register_token_key(token=token)
    data = Redis.hgetall(name=redis_template)
    user, _ = User.objects.get_or_create(
        cellphone=data["cellphone"], first_name=data["first_name"], last_name=data["last_name"], email=data["email"]
    )
    user.set_password(password)
    user.save()
    return user


def generate_login_token(cellphone: str) -> str:
    token = generate_token()
    Redis.set(
        name=RedisKeyTemplates.format_login_token_key(cellphone=cellphone),
        value=token,
        ex=settings.LOGIN_TOKEN_TTL,
    )
    return token
