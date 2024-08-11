from rest_framework.exceptions import Throttled, ValidationError

from accounts.services.rate_limiter import ActionType, RateLimiter


class RateLimitMixin:
    rate_limiter_class = RateLimiter

    def check_rate_limit(self, request, action_type: ActionType):
        identifiers = {
            "ip_address": request.META.get('REMOTE_ADDR'),
            "cellphone": request.data.get('cellphone')
        }

        rate_limiter = self.rate_limiter_class()

        for identifier_type, identifier_value in identifiers.items():
            if rate_limiter.is_blocked(action_type, identifier_value):
                raise Throttled(detail=f"{action_type.value.capitalize()} attempts limit exceeded. Try again later.")

    def handle_invalid_attempt(self, request, action_type: ActionType):
        identifiers = {
            "ip_address": request.META.get('REMOTE_ADDR'),
            "cellphone": request.data.get('cellphone')
        }

        rate_limiter = self.rate_limiter_class()

        for identifier_type, identifier_value in identifiers.items():
            if rate_limiter.increment_attempts(action_type, identifier_value):
                raise Throttled(
                    detail=f"{action_type.value.capitalize()} attempts limit exceeded. You are now blocked.")

    def create(self, request, *args, **kwargs):
        action_type = self.get_action_type()
        self.check_rate_limit(request, action_type)

        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as exc:
            if "invalid_otp" in exc.detail or "invalid_credential" in exc.detail:
                self.handle_invalid_attempt(request, action_type)
            raise exc
