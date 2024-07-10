from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Automation(models.Model):
    class StepsChoices(models.TextChoices):
        AFTER_RECEIVED = "after_received", "After received"
        AFTER_QUOTED = "after_quoted", "After quoted"
        AFTER_DISPATCH = "after_dispatch", "After dispatch"
        AFTER_PICKUP = "after_pickup", "After pick up"
        AFTER_DELIVERY = "after_delivery", "After delivery"
        BEFORE_PICKUP = "before_pickup", "Before pick up"
        BEFORE_DELIVERY = "before_delivery", "Before delivery"

    class StatusChoices(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"

    name = models.CharField(max_length=50)
    email_template = models.ForeignKey("company_management.Template", related_name="+",
                                       on_delete=models.SET_NULL, null=True, blank=True)
    sms_template = models.ForeignKey("company_management.Template", related_name="+",
                                     on_delete=models.SET_NULL, null=True, blank=True)
    steps = models.CharField(max_length=15, choices=StepsChoices.choices)
    delays_minutes = models.IntegerField(default=0)
    status = models.CharField(max_length=10, choices=StatusChoices.choices)
    included_users = models.ManyToManyField(User, '+', blank=True)

    def __str__(self):
        return self.name
