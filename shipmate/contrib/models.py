import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

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


class ConditionChoices(models.TextChoices):
    DRIVES = "run", "Run and drives"
    ROLLS = 'rols', "Inop, it rolls"
    FORKLIFT = 'forklift', "Inop, needs forklift "


class LeadsAbstract(models.Model):
    guid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(editable=False)
    status = models.CharField(max_length=20, choices=LeadsStatusChoices.choices, default=LeadsStatusChoices.LEADS)
    customer = models.ForeignKey("customers.Customer", on_delete=models.SET_NULL, null=True)
    vehicle = models.ForeignKey("cars.CarsModel", on_delete=models.SET_NULL, null=True)
    vehicle_year = models.PositiveSmallIntegerField()
    price = models.PositiveIntegerField(default=0)
    condition = models.CharField(max_length=50, choices=ConditionChoices.choices, default=ConditionChoices.DRIVES)
    trailer_type = models.CharField(choices=TrailerTypeChoices.choices, default=TrailerTypeChoices.OPEN, max_length=20)
    notes = models.TextField(blank=True)

    reservation_price = models.PositiveIntegerField(default=200)
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


class QuoteAbstract(LeadsAbstract):
    status = models.CharField(max_length=20, choices=QuoteStatusChoices.choices, default=QuoteStatusChoices.QUOTES)
    # Payments
    payment_total_tariff = models.PositiveIntegerField(default=0)
    payment_reservation = models.PositiveIntegerField(default=0)
    payment_paid_reservation = models.PositiveIntegerField(default=0)
    payment_carrier_pay = models.PositiveIntegerField(default=0)
    payment_cod_to_carrier = models.PositiveIntegerField(default=0)
    payment_paid_to_carrier = models.PositiveIntegerField(default=0)

    # Date

    date_est_pu = models.DateField(null=True, blank=True)
    date_est_del = models.DateField(null=True, blank=True)
    date_dispatched = models.DateField(null=True, blank=True)
    date_picked_up = models.DateField(null=True, blank=True)
    date_delivered = models.DateField(null=True, blank=True)

    class Meta:
        default_related_name = 'quotes'
        abstract = True


class OrderAbstract(QuoteAbstract):
    ...

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

    title = models.CharField(500)
    second_title = models.CharField(max_length=150, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=10, choices=TypesChoices.choices)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    marked = models.BooleanField(default=False)
    link = models.BigIntegerField(help_text="Link to base attachment ID")  # NOTE: this field for another ATTACHMENT CLASS

    class Meta:
        abstract = True
