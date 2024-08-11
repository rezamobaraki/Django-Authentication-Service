from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response

from core.settings.django.base import BLOCK_DURATION, LOGIN_ATTEMPT_LIMIT, REGISTRATION_ATTEMPT_LIMIT
from core.settings.third_parties.redis import Redis
from core.settings.third_parties.redis_templates import RedisKeyTemplates


class RateLimiterMiddleware(MiddlewareMixin):
    def _get_key(self, key_type, identifier):
        if key_type == "login":
            return RedisKeyTemplates.format_login_attempts_key(identifier)
        elif key_type == "register":
            return RedisKeyTemplates.format_register_attempts_key(identifier)

    def _is_blocked(self, key_type, identifier):
        key = self._get_key(key_type, identifier)
        block_key = RedisKeyTemplates.format_rate_limiter_key(key=key)
        if Redis.exists(block_key):
            return True
        return False

    def _increment_attempts(self, key_type, identifier):
        key = self._get_key(key_type, identifier)
        attempts = Redis.incr(key)
        Redis.expire(key, BLOCK_DURATION)

        return attempts

    def _block(self, key_type, identifier):
        key = self._get_key(key_type, identifier)
        block_key = RedisKeyTemplates.format_rate_limiter_key(key=key)
        Redis.set(block_key, 1, ex=BLOCK_DURATION)

    def _handle_blocking(self, request, key_type, identifier):
        if self._is_blocked(key_type, identifier):
            message = _("Too many attempts, please try again later.")
            return Response({"error": message}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        attempts = self._increment_attempts(key_type, identifier)

        limit = LOGIN_ATTEMPT_LIMIT if key_type == "login" else REGISTRATION_ATTEMPT_LIMIT

        if attempts > limit:
            self._block(key_type, identifier)
            message = _("Too many attempts, please try again later.")
            return Response({"error": message}, status=status.HTTP_429_TOO_MANY_REQUESTS)

    def process_view(self, request, view_func, view_args, view_kwargs):
        if 'login' in request.path:
            ip_address = request.META.get('REMOTE_ADDR')
            username = request.POST.get('username')

            block_response = self._handle_blocking(request, "login", ip_address)
            if block_response:
                return block_response

            block_response = self._handle_blocking(request, "login", username)
            if block_response:
                return block_response

        elif 'register' in request.path:
            ip_address = request.META.get('REMOTE_ADDR')
            cellphone = request.POST.get('cellphone')

            block_response = self._handle_blocking(request, "register", ip_address)
            if block_response:
                return block_response

            block_response = self._handle_blocking(request, "register", cellphone)
            if block_response:
                return block_response

        return None
