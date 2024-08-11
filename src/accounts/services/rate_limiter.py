import time

from core.settings.django.base import BLOCK_DURATION, LOGIN_ATTEMPT_LIMIT, REGISTRATION_ATTEMPT_LIMIT
from core.settings.third_parties.redis import Redis
from core.settings.third_parties.redis_templates import RedisKeyTemplates


class RateLimiter:
    @staticmethod
    def _is_rate_limited(key: str, limit: int) -> bool:
        current_time = int(time.time())
        key_name = RedisKeyTemplates.format_rate_limiter_key(key=key)

        Redis.zremrangebyscore(key_name, 0, current_time - BLOCK_DURATION)
        Redis.zadd(key_name, {current_time: current_time})
        Redis.expire(key_name, BLOCK_DURATION)

        return Redis.zcard(key_name) > REGISTRATION_ATTEMPT_LIMIT

    @classmethod
    def login_attempt(cls, cellphone: str, ip: str) -> bool:
        login_attempts_key = RedisKeyTemplates.format_login_attempts_key(identifier=cellphone)
        ip_key = RedisKeyTemplates.format_login_attempts_key(identifier=ip)

        is_phone_limit = cls._is_rate_limited(login_attempts_key, LOGIN_ATTEMPT_LIMIT)
        is_ip_limit = cls._is_rate_limited(ip_key, LOGIN_ATTEMPT_LIMIT)
        return not (is_phone_limit or is_ip_limit)

    @classmethod
    def register_attempt(cls, cellphone: str, ip: str) -> bool:
        register_attempts_key = RedisKeyTemplates.format_register_attempts_key(identifier=cellphone)
        ip_key = RedisKeyTemplates.format_register_attempts_key(identifier=ip)

        is_phone_limit = cls._is_rate_limited(register_attempts_key, REGISTRATION_ATTEMPT_LIMIT)
        is_ip_limit = cls._is_rate_limited(ip_key, REGISTRATION_ATTEMPT_LIMIT)
        return not (is_phone_limit or is_ip_limit)

    @classmethod
    def check_limit(cls, action, cellphone=None, ip=None):
        if action == 'login':
            return cls.login_attempt(cellphone, ip)
        elif action == 'register':
            return cls.register_attempt(cellphone, ip)
