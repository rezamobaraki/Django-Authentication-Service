from rest_framework.exceptions import APIException, Throttled

from common.services.rate_limiter.constants import ActionType, ERROR_MESSAGES
from common.services.rate_limiter.rate_limiter import RateLimiter


class RateLimitMixin:
    rate_limiter_class = RateLimiter
    rate_limiter_action: str = None

    def check_rate_limit(self, request, action_type: str):
        identifiers = {
            "ip_address": request.META.get('REMOTE_ADDR'),
            "cellphone": request.data.get('cellphone')
        }

        rate_limiter = self.rate_limiter_class()

        for identifier_type, identifier_value in identifiers.items():
            is_blocked, wait_time = rate_limiter.is_blocked(action_type, identifier_value)
            if is_blocked:
                raise Throttled(detail=ERROR_MESSAGES[action_type].format(wait_time=wait_time))

    def handle_invalid_attempt(self, request):
        identifiers = {
            "ip_address": request.META.get('REMOTE_ADDR'),
            "cellphone": request.data.get('cellphone')
        }

        rate_limiter = self.rate_limiter_class()

        for identifier_type, identifier_value in identifiers.items():

            if rate_limiter.increment_attempts(self.rate_limiter_action, identifier_value):
                raise Throttled(detail=ERROR_MESSAGES["blocked"])

    def create(self, request, *args, **kwargs):
        # TODO : Fix this
        # if not isinstance(self.rate_limiter_action, str):
        #     raise APIException("Rate limiter action is not defined")

        if self.rate_limiter_action not in ActionType.values():
            return super().create(request, *args, **kwargs)

        self.check_rate_limit(request, self.rate_limiter_action)

        return super().create(request, *args, **kwargs)
