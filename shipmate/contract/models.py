from django.contrib.auth import get_user_model
from django.db import models

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
        if self.is_default:
            type(self).objects.filter(is_default=True).update(is_default=False)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        last_created = type(self).objects.exclude(id=self.id).order_by('-created_at').first()
        if last_created:
            last_created.is_default = True
            last_created.save()
        super().delete(*args, **kwargs)

    def validate_single_default(self):
        pass


class Ground(BaseContract):
    pass


class Hawaii(BaseContract):
    pass


class International(BaseContract):
    pass
