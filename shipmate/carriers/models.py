from django.db import models


class Carrier(models.Model):
    class CarrierStatus(models.TextChoices):
        FAVORITE = "favorite", "Favorite"
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"
        BLOCKED = "blocked", "Blocked"

    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    location = models.ForeignKey("addresses.City", on_delete=models.CASCADE, related_name="carriers")
    mc_number = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    phone_2 = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField()
    fax = models.CharField(max_length=20)
    status = models.CharField(max_length=8, choices=CarrierStatus.choices, default=CarrierStatus.INACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Carrier"
        verbose_name_plural = "Carriers"

    def __str__(self):
        return self.name


class CarrierDispatcher(models.Model):
    ...
