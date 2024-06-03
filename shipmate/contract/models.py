from django.contrib.auth import get_user_model
from django.db import models
from django.core.exceptions import ValidationError

User = get_user_model()


class GroundStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"


class BaseContract(models.Model):
    name = models.CharField(max_length=255)
    is_default = models.BooleanField(default=True)
    status = models.CharField(choices=GroundStatus.choices, max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    body = models.TextField()

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="+",
                                   null=True, blank=True, editable=False)
    updated_from = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="+",
                                     null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.validate_single_default()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.is_default and not type(self).objects.filter(is_default=True).exclude(id=self.id).exists():
            raise ValidationError('There must be at least one default ground.')
        super().delete(*args, **kwargs)

    def validate_single_default(self):
        if self.is_default:
            default_contract = type(self).objects.filter(is_default=True).exclude(id=self.id).first()
            if default_contract:
                raise ValidationError('There can only be one default ground.')
        else:
            if not type(self).objects.filter(is_default=True).exclude(id=self.id).exists():
                raise ValidationError('There must be at least one default ground.')


class Ground(BaseContract):
    pass


class Hawaii(BaseContract):
    pass


class International(BaseContract):
    pass
