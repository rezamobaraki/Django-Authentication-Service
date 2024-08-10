from django.core.validators import RegexValidator
from django.utils.regex_helper import _lazy_re_compile
from django.utils.translation import gettext_lazy as _

cellphone_validator = RegexValidator(
    _lazy_re_compile(r"^\+989\d{9}$"),
    message=_("invalid_cellphone"),
    code="invalid_cellphone",
)
