from core.settings.django.base import RATE_LIMITER_ATTEMPT_LIMIT, RATE_LIMITER_BLOCK_DURATION
from core.settings.third_parties.redis import Redis
from core.settings.third_parties.redis_templates import RedisKeyTemplates


class RateLimiter:
    def __init__(self):
        self.redis = Redis

    def _get_user_block_key(self, identifier: str) -> str:
        return RedisKeyTemplates.format_user_block_key(identifier)

    def is_user_blocked(self, identifier: str) -> (bool, int):
        block_key = self._get_user_block_key(identifier)
        ttl = self.redis.ttl(block_key)
        is_blocked = ttl > 0
        return is_blocked, ttl

    def increment_attempts(self, identifier: str) -> bool:
        attempts_key = RedisKeyTemplates.format_attempts_key(identifier)
        attempts = self.redis.incr(attempts_key)
        self.redis.expire(attempts_key, RATE_LIMITER_BLOCK_DURATION)

        if attempts > RATE_LIMITER_ATTEMPT_LIMIT:
            block_key = self._get_user_block_key(identifier)
            self.redis.set(block_key, 1, ex=RATE_LIMITER_BLOCK_DURATION)
            return True

        return False
