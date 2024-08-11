from core.settings.third_parties.redis import Redis
from core.settings.third_parties.redis_templates import RedisKeyTemplates


def verify_registration_otp(cellphone: str, input_otp: str) -> bool:
    stored_otp = Redis.get(name=RedisKeyTemplates.format_register_otp_key(cellphone=cellphone))
    return stored_otp == input_otp


def get_cellphone_by_registration_token(input_token: str) -> bool:
    return Redis.get(name=RedisKeyTemplates.format_register_token_key(token=input_token))


def verify_registration_information_token(input_token: str):
    name = RedisKeyTemplates.format_register_information_key(token=input_token)
    return Redis.hget(name=name, key='token') == input_token


def verify_login_token(cellphone: str, input_token: str) -> bool:
    stored_token = Redis.get(name=RedisKeyTemplates.format_login_token_key(cellphone=cellphone))
    return stored_token == input_token
