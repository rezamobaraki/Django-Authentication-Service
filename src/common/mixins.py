from rest_framework.exceptions import Throttled, ValidationError

from accounts.services.rate_limiter import RateLimiter
from .constants import ActionType, ERROR_MESSAGES, INVALID_ERRORS


class RateLimitMixin:
    rate_limiter_class = RateLimiter

    def check_rate_limit(self, request, action_type: ActionType):
        identifiers = {
            "ip_address": request.META.get('REMOTE_ADDR'),
            "cellphone": request.data.get('cellphone')
        }

        rate_limiter = self.rate_limiter_class()

        for identifier_type, identifier_value in identifiers.items():
            is_blocked, wait_time = rate_limiter.is_blocked(action_type, identifier_value)
            if is_blocked:
                raise Throttled(detail=ERROR_MESSAGES[action_type].format(wait_time=wait_time))

    def handle_invalid_attempt(self, request, action_type: ActionType):
        identifiers = {
            "ip_address": request.META.get('REMOTE_ADDR'),
            "cellphone": request.data.get('cellphone')
        }

        rate_limiter = self.rate_limiter_class()

        for identifier_type, identifier_value in identifiers.items():
            if rate_limiter.increment_attempts(action_type, identifier_value):
                raise Throttled(detail=ERROR_MESSAGES["blocked"])

    def create(self, request, *args, **kwargs):
        self.check_rate_limit(request, self.action)

        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as exc:
            # Increment only if certain errors occur
            for error_key in INVALID_ERRORS.keys():
                if error_key in exc.detail:
                    self.handle_invalid_attempt(request, action_type)
            raise exc
