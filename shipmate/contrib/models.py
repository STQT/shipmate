from django.db import models


class TrailerTypeChoices(models.TextChoices):
    OPEN = "open", "Open"
    CLOSE = "enclosed", "Enclosed"


class QuoteStatusChoices(models.TextChoices):
    QUOTES = "quote", "Quote"
    FOLLOWUP = "followUp", "Follow up"
    WARM = "warm", "Warm"
    ONGOING = "ongoing", "Ongoin"
    UPCOMING = "upcoming", "Upcoming"
    ONHOLD = "onHold", "On hold"
    NOTNOW = "notNow", "Not now"


class QuoteConditionChoices(models.TextChoices):
    DRIVES = "run", "Run and drives"
    ROLLS = 'rols', "Inop, it rolls"
    FORKLIFT = 'forklift', "Inop, needs forklift "


class LeadsAbstract(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey("customers.Customer", on_delete=models.SET_NULL, null=True)
    vehicle = models.ForeignKey("cars.CarsModel", on_delete=models.SET_NULL, null=True)
    vehicle_year = models.PositiveSmallIntegerField()
    price = models.PositiveIntegerField(default=0)

    reservation = models.PositiveIntegerField(default=200)
    trailer_type = models.CharField(choices=TrailerTypeChoices.choices, default=TrailerTypeChoices.OPEN, max_length=20)
    date_est_ship = models.DateField(null=True, blank=True)
    is_archive = models.BooleanField(default=False, verbose_name='Is Archived')

    class Meta:
        default_related_name = 'leads'
        abstract = True


class QuoteAbstract(LeadsAbstract):
    condition = models.CharField(max_length=50, choices=QuoteConditionChoices.choices,
                                 blank=True, null=True)
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
