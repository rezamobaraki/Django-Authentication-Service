# src/accounts/apis/authentication.py

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from accounts.serializers.authentication import (
    AuthenticationRequestSerializer, LoginSerializer, RegistrationCompletionSerializer,
    RegistrationInformationSerializer, RegistrationVerificationSerializer
)
from common.viewsets import CreateModelWithFixStatusViewSet

User = get_user_model()


class AuthenticationViewSet(CreateModelWithFixStatusViewSet):
    authentication_classes = []
    permission_classes = []
    serializer_class = AuthenticationRequestSerializer
    fix_status = status.HTTP_200_OK


class RegistrationViewSet(CreateModelWithFixStatusViewSet):
    authentication_classes = []
    permission_classes = []
    serializer_class = None
    fix_status = status.HTTP_200_OK

    def get_serializer_class(self):
        if self.action == 'verify_registration':
            return RegistrationVerificationSerializer
        if self.action == 'submit_registration_information':
            return RegistrationInformationSerializer
        if self.action == 'complete_registration':
            return RegistrationCompletionSerializer
        return super().get_serializer_class()

    @action(detail=False, methods=['POST'], serializer_class=RegistrationVerificationSerializer)
    def verify(self, request, *args, **kwargs):
        return super().create(request, args, kwargs)

    @action(detail=False, methods=['POST'], serializer_class=RegistrationInformationSerializer)
    def information(self, request, *args, **kwargs):
        return super().create(request, args, kwargs)

    @action(detail=False, methods=['POST'], serializer_class=RegistrationCompletionSerializer)
    def complete(self, request, *args, **kwargs):
        return super().create(request, args, kwargs)


class LoginViewSet(CreateModelWithFixStatusViewSet):
    authentication_classes = []
    permission_classes = []
    serializer_class = LoginSerializer
    fix_status = status.HTTP_200_OK
