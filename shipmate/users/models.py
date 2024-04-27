from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, EmailField
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from shipmate.users.managers import UserManager


class User(AbstractUser):
    """
    Default custom user model for ShipMate.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    email = EmailField(_("email address"), unique=True)
    username = None  # type: ignore

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})


class Feature(models.Model):
    class MethodChoices(models.TextChoices):
        EDIT = "edit", "Edit"
        VIEW = "view", "View"
        CREATE = "create", "Create"
        DELETE = "delete", "Delete"

    name = models.CharField(max_length=255)
    for_all_data = models.BooleanField(default=False)
    endpoint = models.CharField(max_length=32)
    method = models.CharField(max_length=10, choices=MethodChoices.choices, default=MethodChoices.VIEW)

    def __str__(self):
        return self.name


class Role(models.Model):
    class RoleAccessStatusChoices(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'

    access_name = models.CharField(max_length=255)
    access_status = models.CharField(max_length=10, choices=RoleAccessStatusChoices.choices, default='active')
    included_users = models.ManyToManyField('User', related_name='roles', blank=True)
    included_features = models.ManyToManyField('Feature', related_name='roles', blank=True)

    def __str__(self):
        return self.access_name


class Team(models.Model):
    class TeamStatusChoices(models.TextChoices):
        active = "active", "Active"
        inactive = "inactive", "Inactive"

    name = CharField(max_length=255)
    status = CharField(max_length=10, choices=TeamStatusChoices.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField('User', related_name='teams', blank=True)

    def __str__(self):
        return self.name


class OTPCode(models.Model):
    code = models.CharField(max_length=6)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="otp")

    def __str__(self):
        return f"{self.user} | {self.code}"
