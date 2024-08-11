from core.settings.third_parties.redis import Redis
from core.settings.third_parties.redis_templates import RedisTemplates


def verify_registration_otp(cellphone: str, input_otp: str) -> bool:
    stored_otp = Redis.get(name=RedisTemplates.format_auth_register_otp(cellphone=cellphone))
    return stored_otp == input_otp


def get_cellphone_by_registration_token(input_token: str) -> bool:
    return Redis.get(name=RedisTemplates.format_auth_register_token(token=input_token))


def verify_registration_information_token(input_token: str):
    name = RedisTemplates.format_auth_register_information(token=input_token)
    return Redis.hget(name=name, key='token') == input_token


def verify_login_token(cellphone: str, input_token: str) -> bool:
    stored_token = Redis.get(name=RedisTemplates.format_auth_login_token(cellphone=cellphone))
    return stored_token == input_token
