# src/accounts/apis/authentication.py

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action

from accounts.serializers.authentication import (
    AuthenticationRequestSerializer, LoginSerializer, RegistrationCompletionSerializer,
    RegistrationInformationSerializer, RegistrationVerificationSerializer
)
from common.services.rate_limiter.mixin import RateLimitMixin
from common.throttles import AuthenticationRateThrottle
from common.viewsets import CreateModelWithFixStatusViewSet

User = get_user_model()


class AuthenticationViewSet(RateLimitMixin, CreateModelWithFixStatusViewSet):
    authentication_classes = []
    permission_classes = []
    serializer_class = AuthenticationRequestSerializer
    fix_status = status.HTTP_200_OK
    throttle_classes = [AuthenticationRateThrottle]


class RegistrationViewSet(RateLimitMixin, CreateModelWithFixStatusViewSet):
    authentication_classes = []
    permission_classes = []
    serializer_class = None
    fix_status = status.HTTP_200_OK

    @action(detail=False, methods=['POST'], serializer_class=RegistrationVerificationSerializer)
    def verify(self, request, *args, **kwargs):
        self.rate_limiter_action = 'register'
        return super().create(request, args, kwargs)

    @action(detail=False, methods=['POST'], serializer_class=RegistrationInformationSerializer)
    def information(self, request, *args, **kwargs):
        return super().create(request, args, kwargs)

    @action(detail=False, methods=['POST'], serializer_class=RegistrationCompletionSerializer)
    def complete(self, request, *args, **kwargs):
        return super().create(request, args, kwargs)


class LoginViewSet(RateLimitMixin, CreateModelWithFixStatusViewSet):
    authentication_classes = []
    permission_classes = []
    serializer_class = LoginSerializer
    fix_status = status.HTTP_200_OK

    def create(self, request, *args, **kwargs):
        self.rate_limiter_action = 'login'
        return super().create(request, args, kwargs)
