# src/common/mixins.py

from rest_framework.exceptions import Throttled

from accounts.services.rate_limiter import RateLimiter


class RateLimitingMixin:
    """
    Mixin to handle rate limiting for login and registration endpoints.
    """

    rate_limit_key = None
    attempt_limit = None

    def check_rate_limit(self, request):
        if self.rate_limit_key is None or self.attempt_limit is None:
            raise ValueError("rate_limit_key and attempt_limit must be set.")

        # Extract cellphone or IP address based on endpoint type
        cellphone = request.data.get('cellphone', None)
        ip = request.META.get('REMOTE_ADDR', None)

        if not RateLimiter.login_attempt(cellphone=cellphone, ip=ip):
            raise APIException("Rate limit exceeded. Please try again later.")

    def create(self, request, *args, **kwargs):
        self.check_rate_limit(request)
        return super().create(request, *args, **kwargs)