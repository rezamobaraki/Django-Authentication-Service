from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel
from common.validators import cellphone_validator


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None):
        if not phone:
            raise ValueError("Users must have a phone number")
        user = self.model(phone=phone)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None):
        user = self.create_user(phone, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, BaseModel):
    cellphone = models.CharField(
        verbose_name=_("cellphone"), max_length=13, unique=True, validators=[cellphone_validator],
        help_text=_("13 characters only in format +989xxxxxxxxx"),
    )
    first_name = models.CharField(verbose_name=_("first name"), max_length=50, blank=True)
    last_name = models.CharField(verbose_name=_("last name"), max_length=50, blank=True)
    email = models.EmailField(verbose_name=_("email address"), max_length=255, blank=True)
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_admin = models.BooleanField(
        verbose_name=_("admin status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )

    objects = UserManager()

    USERNAME_FIELD = 'cellphone'
    EMAIL_FIELD = "email"

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        swappable = "AUTH_USER_MODEL"

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)
