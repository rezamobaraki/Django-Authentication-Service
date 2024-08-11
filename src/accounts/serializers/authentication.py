from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.models import User
from accounts.services.commands.authentication import (
    complete_registration, generate_login_token, generate_registration_token, send_registration_otp,
    store_registration_information
)
from accounts.services.queries.authentication import (
    get_cellphone_by_registration_token, verify_login_token, verify_registration_information_token,
    verify_registration_otp
)
from common.validators import cellphone_validator


class AuthenticationRequestSerializer(serializers.Serializer):
    cellphone = serializers.CharField(validators=[cellphone_validator], write_only=True)
    token = serializers.CharField(read_only=True)
    user_state = serializers.CharField(read_only=True)

    def create(self, validated_data):
        if User.objects.filter(cellphone=validated_data["cellphone"]).exists():
            token = generate_login_token(cellphone=validated_data["cellphone"])
            return {"token": token, "user_state": "old"}
        send_registration_otp(cellphone=validated_data["cellphone"])
        return {"user_state": "new"}


class RegistrationVerificationSerializer(serializers.Serializer):
    code = serializers.CharField(required=True, allow_blank=False, write_only=True)
    cellphone = serializers.CharField(
        required=True, allow_blank=False, write_only=True, validators=[cellphone_validator],
    )
    token = serializers.CharField(read_only=True)

    def validate(self, attrs):
        code_is_valid = verify_registration_otp(cellphone=attrs["cellphone"], input_otp=attrs["code"])
        if not code_is_valid:
            raise serializers.ValidationError(_("invalid_otp"), code="invalid_otp")

        return attrs

    def create(self, validated_data):
        token = generate_registration_token(cellphone=validated_data["cellphone"])
        return {"token": token}


class RegistrationInformationSerializer(serializers.Serializer):
    token = serializers.CharField(required=True, allow_blank=False)
    first_name = serializers.CharField(write_only=True, required=True, allow_blank=False)
    last_name = serializers.CharField(write_only=True, required=True, allow_blank=False)
    email = serializers.EmailField(write_only=True, required=True, allow_blank=True)

    def validate(self, attrs):
        cellphone = get_cellphone_by_registration_token(input_token=attrs["token"])
        if not cellphone:
            raise serializers.ValidationError(_("invalid_token"), code="invalid_token")
        attrs["cellphone"] = cellphone
        return attrs

    def create(self, validated_data):
        token = store_registration_information(
            cellphone=validated_data["cellphone"], first_name=validated_data["first_name"],
            last_name=validated_data["last_name"], email=validated_data.get("email"),
        )
        return {"token": token}


class RegistrationCompletionSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True, allow_blank=False)
    token = serializers.CharField(write_only=True, required=True, allow_blank=False)

    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate_token(self, value):
        if not verify_registration_information_token(input_token=value):
            raise serializers.ValidationError(_("invalid_token"), code="invalid_token")
        return value

    def create(self, validated_data):
        user = complete_registration(token=validated_data["token"], password=validated_data["password"])
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

        if not verify_login_token(cellphone=attrs["cellphone"], input_token=attrs["token"]):
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
