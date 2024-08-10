from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.models import User
from accounts.services.commands.authentication import (
    authentication_login_token, authentication_register_complete, authentication_register_information,
    authentication_register_send_otp, authentication_register_token
)
from accounts.services.queries.authentication import (
    authentication_login_verify_token, authentication_register_retrieve_cellphone_with_token,
    authentication_register_verify_information_token, authentication_register_verify_otp
)
from common.validators import cellphone_validator


class AuthSerializer(serializers.Serializer):
    cellphone = serializers.CharField(validators=[cellphone_validator], write_only=True)
    token = serializers.CharField(read_only=True)
    user_state = serializers.CharField(read_only=True)

    def create(self, validated_data):
        if User.objects.filter(cellphone=validated_data["cellphone"]).exists():
            token = authentication_login_token(cellphone=validated_data["cellphone"])
            return {"token": token, "user_state": "old"}
        authentication_register_send_otp(cellphone=validated_data["cellphone"])
        return {"user_state": "new"}


class RegisterVerifySerializer(serializers.Serializer):
    code = serializers.CharField(required=True, allow_blank=False, write_only=True)
    cellphone = serializers.CharField(
        required=True, allow_blank=False, write_only=True, validators=[cellphone_validator],
    )
    token = serializers.CharField(read_only=True)

    def validate(self, attrs):
        code_is_valid = authentication_register_verify_otp(cellphone=attrs["cellphone"], input_otp=attrs["code"])
        if not code_is_valid:
            raise serializers.ValidationError(_("invalid_otp"), code="invalid_otp")

        return attrs

    def create(self, validated_data):
        token = authentication_register_token(cellphone=validated_data["cellphone"])
        return {"token": token}


class RegisterInformationSerializer(serializers.Serializer):
    token = serializers.CharField(required=True, allow_blank=False)
    first_name = serializers.CharField(write_only=True, required=True, allow_blank=False)
    last_name = serializers.CharField(write_only=True, required=True, allow_blank=False)
    email = serializers.EmailField(write_only=True, required=True, allow_blank=True)

    def validate(self, attrs):
        cellphone = authentication_register_retrieve_cellphone_with_token(input_token=attrs["token"])
        if not cellphone:
            raise serializers.ValidationError(_("invalid_token"), code="invalid_token")
        attrs["cellphone"] = cellphone
        return attrs

    def create(self, validated_data):
        token = authentication_register_information(
            cellphone=validated_data["cellphone"], first_name=validated_data["first_name"],
            last_name=validated_data["last_name"], email=validated_data.get("email"),
        )
        return {"token": token}


class RegisterCompleteSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True, allow_blank=False)
    token = serializers.CharField(write_only=True, required=True, allow_blank=False)

    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate_token(self, value):
        if not authentication_register_verify_information_token(input_token=value):
            raise serializers.ValidationError(_("invalid_token"), code="invalid_token")
        return value

    def create(self, validated_data):
        user = authentication_register_complete(token=validated_data["token"], password=validated_data["password"])
        refresh_token = TokenObtainPairSerializer.get_token(user)
        refresh = str(refresh_token)
        access = str(refresh_token.access_token)

        return {"access": access, "refresh": refresh}


class LoginSerializer(serializers.Serializer):
    cellphone = serializers.CharField(write_only=True, required=True, validators=[cellphone_validator])
    token = serializers.CharField(write_only=True, required=True, allow_blank=False)
    password = serializers.CharField(write_only=True, required=True, allow_blank=False)

    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, attrs):
        user = User.objects.filter(cellphone=attrs["cellphone"]).first()

        if not authentication_login_verify_token(cellphone=attrs["cellphone"], input_token=attrs["token"]):
            raise serializers.ValidationError(_("invalid_token"), code="invalid_token")

        if not user or not user.check_password(raw_password=attrs["password"]):
            raise serializers.ValidationError(_("invalid_credential"), code="invalid_credential")

        attrs["user"] = user
        return attrs

    def create(self, validated_data):
        user = validated_data["user"]
        refresh_token = TokenObtainPairSerializer.get_token(user)
        refresh = str(refresh_token)
        access = str(refresh_token.access_token)

        return {"access": access, "refresh": refresh}
