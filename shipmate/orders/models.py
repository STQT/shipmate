from django.contrib.auth import get_user_model
from django.db import models

from shipmate.contrib.models import Attachments, OrderAbstract, VehicleAbstract
from shipmate.utils.models import BaseLog

User = get_user_model()


class OrderLocationTypeChoices(models.TextChoices):
    R2R = "r2r", "Residential to residential"
    R2B = "r2b", "Residential to business"
    B2R = "b2r", "Business to residential"
    B2B = "b2b", "Business to business"


class Order(OrderAbstract):
    class DispatchPaidByChoices(models.TextChoices):
        CARRIER = "carrier", "COD to Carrier"
        DELIVERY = "delivery", "COD to Delivery Terminal"
        PICKUP = "pickup", "COD to Pickup Terminal"
        ONPICKUP = "onpickup", "COP to Carrier (On Pickup)"
        INVOICE = "invoice", "Shipper Invoice"
        PREPAYMENT = "prepayment", "Additional Shipper Pre-payment"

    class DispatchPaymentTermChoices(models.TextChoices):
        IMMEDIATELY = "immediately", "Immediately"
        TWO = "2days", "2 business days"
        FIVE = "5days", "5 business days"
        TEN = "10days", "10 business days"
        FIFTEEN = "15days", "15 business days"
        THIRTY = "30days", "30 business days"

    class DispatchTermsChoices(models.TextChoices):
        PICKUP = "pickup", "Pickup"
        DELIVERY = "delivery", "Delivery"
        SIGNED = "signed", "Receiving a signed Bill of Lading"

    class DispatchCodMethodChoices(models.TextChoices):
        CASH = "cash", "Cash/Certified Funds"
        CHECK = "check", "Check"

    class DispatchPaymentTypeChoices(models.TextChoices):
        CASH = "cash", "Cash"
        FUND = "fund", "Certified fund"
        CHECK = "check", "Company check"
        ACH = "ach", "ACH"
        ZELLE = "zelle", "Zelle"
        VENMO = "venmo", "Venmo"
        CASHAPP = "cashapp", "CashApp"

    buyer_number = models.CharField(max_length=50, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_user')
    extra_user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,
                                   related_name='order_extra_user')
    location_type = models.CharField(max_length=3,
                                     choices=OrderLocationTypeChoices.choices)

    carrier = models.ForeignKey("carriers.Carrier", on_delete=models.SET_NULL, related_name="orders",
                                null=True, blank=True)
    dispatch_paid_by = models.CharField(max_length=10, null=True, blank=True, choices=DispatchPaidByChoices.choices)
    dispatch_payment_term = models.CharField(max_length=11, null=True, blank=True,
                                             choices=DispatchPaymentTermChoices.choices)
    dispatch_term_begins = models.CharField(max_length=10, null=True, blank=True,
                                            choices=DispatchTermsChoices.choices)
    dispatch_cod_method = models.CharField(max_length=5, null=True, blank=True,
                                           choices=DispatchCodMethodChoices.choices)
    dispatch_payment_type = models.CharField(max_length=10, null=True, blank=True,
                                             choices=DispatchPaymentTypeChoices.choices)

    # origin
    origin = models.ForeignKey("addresses.City", on_delete=models.SET_NULL, null=True, related_name='orders_origin')
    origin_address = models.CharField(max_length=255)
    origin_business_name = models.CharField(max_length=255, null=True, blank=True)
    origin_business_phone = models.CharField(max_length=50, null=True, blank=True)
    origin_contact_person = models.CharField(max_length=255, null=True, blank=True)
    origin_phone = models.CharField(max_length=50, null=True, blank=True)
    origin_second_phone = models.CharField(max_length=50, null=True, blank=True)
    origin_buyer_number = models.CharField(max_length=50, null=True, blank=True)

    # destination
    destination = models.ForeignKey("addresses.City", on_delete=models.SET_NULL, null=True,
                                    related_name='orders_destination')
    destination_address = models.CharField(max_length=255)
    destination_business_name = models.CharField(max_length=255, null=True, blank=True)
    destination_business_phone = models.CharField(max_length=50, null=True, blank=True)
    destination_contact_person = models.CharField(max_length=255, null=True, blank=True)
    destination_phone = models.CharField(max_length=50, null=True, blank=True)
    destination_second_phone = models.CharField(max_length=50, null=True, blank=True)
    destination_buyer_number = models.CharField(max_length=50, null=True, blank=True)

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

    updated_from = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="+",
                                     null=True, blank=True)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"


class OrderAttachment(Attachments):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

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


class OrderLog(BaseLog):
    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name="logs")


class OrderContract(models.Model):
    class TypeChoices(models.TextChoices):
        HAWAII = "hawaii", "Hawaii"
        GROUND = "ground", "Ground"
        INTERNATIONAL = "international", "International"

    order = models.ForeignKey("Order", to_field="guid", on_delete=models.CASCADE, related_name="contracts")
    created_at = models.DateTimeField(auto_now_add=True)
    signed = models.BooleanField(default=False)
    contract_type = models.CharField(max_length=13, choices=TypeChoices.choices)

    def __str__(self):
        return self.contract_type
