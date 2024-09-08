import uuid

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from shipmate.utils.models import BaseLog

User = get_user_model()


class TrailerTypeChoices(models.TextChoices):
    OPEN = "open", "Open"
    CLOSE = "enclosed", "Enclosed"


class LeadsStatusChoices(models.TextChoices):
    LEADS = "leads", "Leads"
    ARCHIVED = "archived", "Archived"


class QuoteStatusChoices(models.TextChoices):
    QUOTES = "quote", "Quote"
    FOLLOWUP = "followUp", "Follow up"
    WARM = "warm", "Warm"
    ONGOING = "ongoing", "Ongoin"
    UPCOMING = "upcoming", "Upcoming"
    ONHOLD = "onHold", "On hold"
    NOTNOW = "notNow", "Not now"
    ARCHIVED = "archived", "Archived"


class OrderStatusChoices(models.TextChoices):
    ORDERS = "orders", "Orders"
    BOOKED = "booked", "Booked"
    POSTED = "posted", "Posted"
    NOTSIGNED = "notsigned", "Not-Signed"
    DISPATCHED = "dispatched", "Dispatched"
    ISSUE = "issue", "Issue"
    PICKEDUP = "pickedup", "Picked up"
    COMPLETED = "completed", "Completed"
    ONHOLD = "onhold", "On hold"
    ARCHIVED = "archived", "Archived"


class ConditionChoices(models.TextChoices):
    DRIVES = "run", "Run and drives"
    ROLLS = 'rols', "Inop, it rolls"
    # FORKLIFT = 'forklift', "Inop, needs forklift "


class VehicleAbstract(models.Model):
    vehicle = models.ForeignKey("cars.CarsModel", on_delete=models.SET_NULL, null=True)
    vehicle_year = models.PositiveSmallIntegerField()

    class Meta:
        default_related_name = 'vehicles'
        abstract = True


def validate_positive(value):
    if value < 0:
        raise ValidationError('Price must be a positive number.')


class LeadsAbstract(models.Model):
    guid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(editable=False)
    status = models.CharField(max_length=20, choices=LeadsStatusChoices.choices, default=LeadsStatusChoices.LEADS)
    customer = models.ForeignKey("customers.Customer", on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2, validators=[validate_positive])
    condition = models.CharField(max_length=50, choices=ConditionChoices.choices, default=ConditionChoices.DRIVES)
    trailer_type = models.CharField(choices=TrailerTypeChoices.choices, default=TrailerTypeChoices.OPEN, max_length=20)
    notes = models.TextField(blank=True)

    reservation_price = models.DecimalField(default=0, max_digits=10, decimal_places=2, validators=[validate_positive])
    date_est_ship = models.DateField()
    source = models.ForeignKey("lead_managements.Provider", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        default_related_name = 'leads'
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk:
            # Object is being created, set created_at and updated_at
            self.created_at = timezone.now()
            self.updated_at = self.created_at
        else:
            # Object is being updated
            old_instance = self.__class__.objects.get(pk=self.pk)
            if self.status != old_instance.status:
                # Status changed, update updated_at
                self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    @property
    def customer_name(self):
        customer = self.customer
        if not self.customer:
            return "NaN"
        name = customer.name
        last_name = customer.last_name if customer.last_name else ""
        return name + " " + last_name

    @property
    def customer_phone(self):
        phone = self.customer.phone if self.customer else "NaN"
        if phone and len(phone) == 10:  # Assuming phone is a 10-digit number
            return f"({phone[:3]}) {phone[3:6]}-{phone[6:]}"
        return phone


class QuoteAbstract(LeadsAbstract):
    status = models.CharField(max_length=20, choices=QuoteStatusChoices.choices, default=QuoteStatusChoices.QUOTES)

    class Meta:
        default_related_name = 'quotes'
        abstract = True


class OrderAbstract(QuoteAbstract):
    status = models.CharField(max_length=20, choices=OrderStatusChoices.choices, default=OrderStatusChoices.ORDERS)

    class Meta:
        default_related_name = 'orders'
        abstract = True


class Attachments(models.Model):
    class TypesChoices(models.TextChoices):
        NOTE = "note", "Note"
        ACTIVITY = "activity", "Activity"
        TASK = "task", "Task"  # API
        PHONE = "phone", "Phone"  # API
        EMAIL = "email", "Email"  # API
        FILE = "file", "File"  # API

    title = models.TextField()
    second_title = models.CharField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=10, choices=TypesChoices.choices)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    marked = models.BooleanField(default=False)
    link = models.BigIntegerField(help_text="Link to base attachment ID")
    file = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class UserLog(BaseLog):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="logs")
