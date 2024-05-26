from django.contrib.auth import get_user_model
from django.db import models

from shipmate.contrib.models import Attachments, OrderAbstract, VehicleAbstract

User = get_user_model()


class OrderLocationTypeChoices(models.TextChoices):
    R2R = "r2r", "Residential to residential"
    R2B = "r2b", "Residential to business"
    B2R = "b2r", "Business to residential"
    B2B = "b2b", "Business to business"


class Order(OrderAbstract):
    buyer_number = models.CharField(max_length=50, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_user')
    extra_user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,
                                   related_name='order_extra_user')
    location_type = models.CharField(max_length=3,
                                     choices=OrderLocationTypeChoices.choices)
    carrier = models.ForeignKey("carriers.Carrier", on_delete=models.CASCADE, related_name="orders",
                                null=True, blank=True)

    # origin
    origin = models.ForeignKey("addresses.City", on_delete=models.SET_NULL, null=True, related_name='orders_origin')
    origin_business_name = models.CharField(max_length=255, null=True, blank=True)
    origin_business_phone = models.CharField(max_length=50, null=True, blank=True)
    origin_contact_person = models.CharField(max_length=255, null=True, blank=True)
    origin_phone = models.CharField(max_length=50, null=True, blank=True)
    origin_second_phone = models.CharField(max_length=50, null=True, blank=True)
    origin_buyer_number = models.CharField(max_length=50, null=True, blank=True)

    # destination
    destination = models.ForeignKey("addresses.City", on_delete=models.SET_NULL, null=True,
                                    related_name='orders_destination')
    destination_business_name = models.CharField(max_length=255, null=True, blank=True)
    destination_business_phone = models.CharField(max_length=50, null=True, blank=True)
    destination_contact_person = models.CharField(max_length=255, null=True, blank=True)
    destination_phone = models.CharField(max_length=50, null=True, blank=True)
    destination_second_phone = models.CharField(max_length=50, null=True, blank=True)

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

    cd_note = models.CharField(max_length=255, null=True, blank=True)
    cm_note = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"


class OrderAttachment(Attachments):
    lead = models.ForeignKey(Order, on_delete=models.CASCADE)

    class Meta:
        default_related_name = "orders"


class OrderVehicles(VehicleAbstract):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    lot = models.CharField(max_length=20, null=True, blank=True)
    vin = models.CharField(max_length=50, null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True)
    plate = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        default_related_name = "order_vehicles"
