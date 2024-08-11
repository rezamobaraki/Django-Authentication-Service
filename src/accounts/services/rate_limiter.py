from common.constants import ActionType, ATTEMPT_LIMITS
from core.settings.django.base import BLOCK_DURATION
from core.settings.third_parties.redis import Redis
from core.settings.third_parties.redis_templates import RedisKeyTemplates


class RateLimiter:
    def __init__(self):
        self.redis = Redis

    def _get_key(self, action_type: ActionType, identifier: str) -> str:
        return getattr(RedisKeyTemplates, f"format_{action_type.value}_attempts_key")(identifier)

    def _get_block_key(self, action_key: str) -> str:
        return RedisKeyTemplates.format_rate_limiter_key(key=action_key)

    def is_blocked(self, action_type: ActionType, identifier: str) -> (bool, int):
        action_key = self._get_key(action_type, identifier)
        block_key = self._get_block_key(action_key)
        ttl = self.redis.ttl(block_key)
        is_blocked = ttl > 0
        return is_blocked, ttl

    def increment_attempts(self, action_type: ActionType, identifier: str) -> bool:
        action_key = self._get_key(action_type, identifier)
        block_key = self._get_block_key(action_key)

        attempts = self.redis.incr(action_key)
        self.redis.expire(action_key, BLOCK_DURATION)

        if attempts > ATTEMPT_LIMITS[action_type]:
            self.redis.set(block_key, 1, ex=BLOCK_DURATION)
            return True

        return False
