from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from accounts.serializers.authentication import (

    LoginSerializer, RegisterInformationSerializer, RegisterPasswordSerializer,
    RegisterVerifySerializer, AuthSerializer,
)
from common.viewsets import CreateModelWithFixStatusViewSet

User = get_user_model()


class AuthViewSet(CreateModelWithFixStatusViewSet):
    authentication_classes = []
    permission_classes = []
    serializer_class = None
    fix_status = status.HTTP_200_OK

    def create(self, request, *args, **kwargs):
        self.serializer_class = AuthSerializer
        return super().create(request, args, kwargs)


class RegisterViewSet(CreateModelWithFixStatusViewSet, GenericViewSet):
    authentication_classes = []
    permission_classes = []
    serializer_class = None
    fix_status = status.HTTP_200_OK

    @action(detail=False, methods=['POST'], serializer_class=RegisterVerifySerializer)
    def verify(self, request, *args, **kwargs):
        return super().create(request, args, kwargs)

    @action(detail=False, methods=['POST'], serializer_class=RegisterInformationSerializer)
    def information(self, request, *args, **kwargs):
        return super().create(request, args, kwargs)

    @action(detail=False, methods=['POST'], serializer_class=RegisterPasswordSerializer)
    def complete(self, request, *args, **kwargs):
        return super().create(request, args, kwargs)


class LoginViewSet(CreateModelWithFixStatusViewSet):
    authentication_classes = []
    permission_classes = []
    serializer_class = LoginSerializer
    fix_status = status.HTTP_200_OK
    # throttle_classes = [LoginRateThrottle]
