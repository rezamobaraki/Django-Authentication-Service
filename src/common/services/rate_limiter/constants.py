from enum import Enum

from django.utils.translation import gettext_lazy as _

from core.settings.django.base import LOGIN_ATTEMPT_LIMIT, REGISTRATION_ATTEMPT_LIMIT


class ActionType(Enum):
    LOGIN = "login"
    REGISTER = "register"
    BLOCKED = "blocked"

    @classmethod
    def values(cls):
        return [action.value for action in cls]


ERROR_MESSAGES = {
    ActionType.LOGIN.value: _("Login attempts limit exceeded. Try again after {wait_time} seconds."),
    ActionType.REGISTER.value: _("Register attempts limit exceeded. Try again after {wait_time} seconds."),
    ActionType.BLOCKED.value: _("You are now blocked due to too many failed attempts."),
}
ATTEMPT_LIMITS = {
    ActionType.LOGIN.value: LOGIN_ATTEMPT_LIMIT,
    ActionType.REGISTER.value: REGISTRATION_ATTEMPT_LIMIT,
}
