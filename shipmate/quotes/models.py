from django.db import models


class Quote(models.Model):
    quoted = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey("customers.Customer", related_name='quotes',
                                 on_delete=models.SET_NULL, null=True)
    phone = models.CharField(max_length=15)
    vehicle = models.ForeignKey("cars.CarsModel", related_name='quotes',
                                on_delete=models.SET_NULL, null=True)
    vehicle_year = models.PositiveSmallIntegerField()
    origin = models.CharField(max_length=25)
    destination = models.CharField(max_length=25)
    price = models.FloatField()

    # Details
    condition = models.CharField(max_length=50, blank=True, null=True)

    # Payments
    payment_total_tariff = models.FloatField(default=0)
    payment_reservation = models.FloatField(default=0)
    payment_paid_reservation = models.FloatField(default=0)
    payment_carrier_pay = models.FloatField(default=0)
    payment_cod_to_carrier = models.FloatField(default=0)
    payment_paid_to_carrier = models.FloatField(default=0)

    # Date
    date_est_ship = models.DateField(null=True, blank=True)
    date_est_pu = models.DateField(null=True, blank=True)
    date_est_del = models.DateField(null=True, blank=True)
    date_dispatched = models.DateField(null=True, blank=True)
    date_picked_up = models.DateField(null=True, blank=True)
    date_delivered = models.DateField(null=True, blank=True)
