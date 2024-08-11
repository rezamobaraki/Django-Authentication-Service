from enum import Enum

from django.utils.translation import gettext_lazy as _

from core.settings.django.base import LOGIN_ATTEMPT_LIMIT, REGISTRATION_ATTEMPT_LIMIT


class ActionType(Enum):
    LOGIN = "login"
    REGISTER = "register"
    BLOCK = "block"


ERROR_MESSAGES = {
    ActionType.LOGIN: _("Login attempts limit exceeded. Try again after {wait_time} seconds."),
    ActionType.REGISTER: _("Registration attempts limit exceeded. Try again after {wait_time} seconds."),
    ActionType.BLOCK: _("You are now blocked due to too many failed attempts."),
}

INVALID_ERRORS = {
    "invalid_otp": "OTP is incorrect.",
    "invalid_credential": "Invalid login credentials.",
}

ATTEMPT_LIMITS = {
    ActionType.LOGIN: LOGIN_ATTEMPT_LIMIT,
    ActionType.REGISTER: REGISTRATION_ATTEMPT_LIMIT,
}
