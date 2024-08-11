from enum import Enum

from core.settings.django.base import BLOCK_DURATION, LOGIN_ATTEMPT_LIMIT, REGISTRATION_ATTEMPT_LIMIT
from core.settings.third_parties.redis import Redis
from core.settings.third_parties.redis_templates import RedisKeyTemplates


class ActionType(Enum):
    LOGIN = "login"
    REGISTER = "register"


class RateLimiter:
    ACTION_LIMITS = {
        ActionType.LOGIN: LOGIN_ATTEMPT_LIMIT,
        ActionType.REGISTER: REGISTRATION_ATTEMPT_LIMIT
    }

    def __init__(self):
        self.redis = Redis

    def _get_key(self, action_type: ActionType, identifier: str) -> str:
        if action_type == ActionType.LOGIN:
            return RedisKeyTemplates.format_login_attempts_key(identifier)
        elif action_type == ActionType.REGISTER:
            return RedisKeyTemplates.format_register_attempts_key(identifier)

    def _get_block_key(self, action_key: str) -> str:
        return RedisKeyTemplates.format_rate_limiter_key(key=action_key)

    def is_blocked(self, action_type: ActionType, identifier: str) -> bool:
        action_key = self._get_key(action_type, identifier)
        block_key = self._get_block_key(action_key)
        return self.redis.exists(block_key)

    def increment_attempts(self, action_type: ActionType, identifier: str) -> bool:
        action_key = self._get_key(action_type, identifier)
        block_key = self._get_block_key(action_key)

        attempts = self.redis.incr(action_key)
        self.redis.expire(action_key, BLOCK_DURATION)

        if attempts > self.ACTION_LIMITS[action_type]:
            self.redis.set(block_key, 1, ex=BLOCK_DURATION)
            return True

        return False
