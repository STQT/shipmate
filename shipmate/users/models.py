import random
import io
from PIL import Image, ImageDraw, ImageFont
from django.core.files.base import ContentFile
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, EmailField
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from shipmate.utils.models import BaseLog
from shipmate.users.managers import UserManager


class User(AbstractUser):
    """
    Default custom user model for ShipMate.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    first_name = CharField(_("First name"), max_length=255, blank=True, null=True)
    last_name = CharField(_("First name"), max_length=255, blank=True, null=True)
    phone = CharField(_("Phone"), max_length=20, blank=True, null=True)
    ext = CharField(_("Ext"), max_length=10, blank=True, null=True)
    email = EmailField(_("email address"), unique=True)
    team = models.ForeignKey("Team", verbose_name="Team",
                             on_delete=models.SET_NULL, blank=True, null=True, related_name="users")
    access = models.ForeignKey("Role", verbose_name="Access",
                               on_delete=models.SET_NULL, blank=True, null=True, related_name="access_users")
    # TODO: fix

    picture = models.ImageField(_("Profile Picture"), upload_to="profile_pictures", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    username = None  # type: ignore

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    updated_from = models.ForeignKey("User", on_delete=models.SET_NULL, related_name="+",
                                     null=True, blank=True)

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})

    def save(self, *args, **kwargs):
        if self.pk is not None:
            old_instance = User.objects.filter(pk=self.pk).first()
            if old_instance:
                old_first_name = old_instance.first_name
                old_last_name = old_instance.last_name
            else:
                old_first_name = None
                old_last_name = None
            old_initials = self.get_initials(old_first_name, old_last_name)
            initials = self.get_initials(self.first_name, self.last_name)
            # Check if the picture needs to be updated
            if not self.picture or old_initials != initials:
                avatar = self.generate_avatar(initials)
                self.picture.save(f"{self.id}.png", ContentFile(avatar), save=False)

        super().save(*args, **kwargs)

    def get_initials(self, first_name, last_name) -> str:
        initials = ""
        initials += first_name[0] if first_name else "A"
        initials += last_name[0] if last_name else "A"
        return initials.upper()

    def generate_avatar(self, text: str, size=100):
        foreground_colors = ['#FFFFFF', '#000000']  # White and Black
        background_colors = ['#E74C3C', '#3498DB', '#2ECC71', '#F1C40F', '#E67E22',
                             '#9B59B6']  # Red, Blue, Green, Yellow, Orange, Purple
        foreground_color = random.choice(foreground_colors)
        background_color = random.choice(background_colors)

        image = Image.new("RGBA", (size, size), background_color)
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default(size=70)
        _, _, text_width, text_height = draw.textbbox((0, 0), text=text, font=font)
        position = ((size - text_width) / 2, (size - text_height - 10) / 2)
        draw.text(position, text, fill=foreground_color, font=font)
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        return buffer.getvalue()


class Feature(models.Model):
    class MethodChoices(models.TextChoices):
        EDIT = "edit", "Edit"
        VIEW = "view", "View"
        CREATE = "create", "Create"
        DELETE = "delete", "Delete"

    # TODO: add endpoint choices

    name = models.CharField(max_length=255)
    for_all_data = models.BooleanField(default=False)  # TODO: remove this
    endpoint = models.CharField(max_length=32)
    method = models.CharField(max_length=10, choices=MethodChoices.choices, default=MethodChoices.VIEW)
    updated_from = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="+",
                                     null=True, blank=True)

    def __str__(self):
        return self.name


class FeatureLog(BaseLog):
    feature = models.ForeignKey("Feature", on_delete=models.CASCADE, related_name="logs")


class Role(models.Model):
    class RoleAccessStatusChoices(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'

    access_name = models.CharField(max_length=255)
    access_status = models.CharField(max_length=10, choices=RoleAccessStatusChoices.choices,
                                     default=RoleAccessStatusChoices.ACTIVE)
    included_features = models.ManyToManyField('Feature', related_name='roles', blank=True)
    updated_from = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="+",
                                     null=True, blank=True)

    def __str__(self):
        return self.access_name


class RoleLog(BaseLog):
    role = models.ForeignKey("Role", on_delete=models.CASCADE, related_name="logs")


class Team(models.Model):
    class TeamStatusChoices(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"

    name = CharField(max_length=255)
    status = CharField(max_length=10, choices=TeamStatusChoices.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_from = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="+",
                                     null=True, blank=True)

    def __str__(self):
        return self.name


class TeamLog(BaseLog):
    team = models.ForeignKey("Team", on_delete=models.CASCADE, related_name="logs")


class OTPCode(models.Model):
    code = models.CharField(max_length=6)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="otp")

    def __str__(self):
        return f"{self.user} | {self.code}"
