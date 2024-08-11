from django.utils.translation import gettext as _
from rest_framework.exceptions import Throttled

from common.services.rate_limiter.rate_limiter import RateLimiter


class RateLimitMixin:
    rate_limiter_class = RateLimiter
    message = _("You are now blocked due to too many failed attempts.")

    def check_user_block(self, request):
        identifiers = {
            "ip_address": request.META.get('REMOTE_ADDR'),
            "cellphone": request.data.get('cellphone')
        }

        rate_limiter = self.rate_limiter_class()

        for identifier_value in identifiers.values():
            is_blocked, wait_time = rate_limiter.is_user_blocked(identifier_value)
            if is_blocked:
                raise Throttled(detail=self.message, wait=wait_time)

    def handle_invalid_attempt(self, request):
        identifiers = {
            "ip_address": request.META.get('REMOTE_ADDR'),
            "cellphone": request.data.get('cellphone')
        }

        rate_limiter = self.rate_limiter_class()

        for identifier_value in identifiers.values():
            if rate_limiter.increment_attempts(identifier_value):
                raise Throttled(detail=self.message)

    def create(self, request, *args, **kwargs):
        self.check_user_block(request)
        return super().create(request, *args, **kwargs)
