import os
from datetime import datetime

from django.db import models


class TypeChoices(models.TextChoices):
    credit_card = "credit_card", "Credit Card"
    zelle = "zelle", "Zelle"
    cashapp = "cashapp", "CashApp"
    venmo = "venmo", "Venmo"
    paypal = "paypal", "PayPal"
    cash = "cash", "Cash"
    cashier = "cashier", "Cashier"
    cashier_check = "cashier_check", "Cashier's check"
    ach = "ach", "ACH"


class OrderPayment(models.Model):
    class NameChoices(models.TextChoices):
        auto_transportation = "auto", "Auto Transportation"
        auto_carrier_fee = "auto_carrier", "Auto Transportation (carrier fee)"
        carrier_fee = "carrier", "Carrier fee"

    class ChargeTypeChoices(models.TextChoices):
        charge = "charge", "Charge"
        refund = "refund", "Refund"
        chargeback = "chargeback", "Chargeback"
        sent = "send", "Send"
        payroll = "payroll", "Payroll"

    class DirectionChoices(models.TextChoices):
        customer_to_broker = "cus2brok", "Customer to Broker"
        broker_to_customer = "brok2cus", "Broker to Customer"
        broker_to_carrier = "brok2car", "Broker to Carrier"
        carrier_to_broker = "car2brok", "Carrier to Broker"
        broker_to_employee = "brok2emp", "Broker to Employee"

    class StatusChoices(models.TextChoices):
        CREATED = "created", "Created"
        PAID = "paid", "Paid"
        CHARGE = "charge", "Charge"

    order = models.ForeignKey("orders.Order", on_delete=models.CASCADE, to_field="guid", related_name="payments")
    name = models.CharField(max_length=12, choices=NameChoices.choices)
    quantity = models.PositiveSmallIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_charged = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=14, choices=TypeChoices.choices)
    surcharge_fee_rate = models.PositiveSmallIntegerField()
    charge_type = models.CharField(max_length=10, choices=ChargeTypeChoices.choices)
    direction = models.CharField(max_length=20, choices=DirectionChoices.choices)
    created_at = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=StatusChoices.choices, default=StatusChoices.CREATED)

    def __str__(self):
        return f"{self.order.pk} | {self.name}"


def upload_to(instance, filename):
    today = datetime.today()
    return os.path.join(
        'payment_attachments',
        str(today.year),
        str(today.month).zfill(2),
        str(today.day).zfill(2),
        filename
    )

def upload_to_cc(instance, filename):
    today = datetime.today()
    return os.path.join(
        'credit_cards',
        str(today.year),
        str(today.month).zfill(2),
        str(today.day).zfill(2),
        filename
    )


class OrderPaymentAttachment(models.Model):
    order_payment = models.ForeignKey(OrderPayment, on_delete=models.CASCADE, related_name="attachments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to=upload_to, blank=True, null=True)
    payment_type = models.CharField(max_length=14, choices=TypeChoices.choices)
    is_success = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=20, null=True, blank=True)
    credit_card = models.ForeignKey("OrderPaymentCreditCard", on_delete=models.DO_NOTHING,
                                    blank=True, null=True, related_name="+")

    def __str__(self):
        return str(self.amount)


class OrderPaymentCreditCard(models.Model):
    order = models.ForeignKey("orders.Order", to_field="guid",
                              on_delete=models.CASCADE, related_name="credit_cards")
    card_number = models.CharField(max_length=16)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    expiration_date = models.CharField(max_length=5)
    cvv = models.CharField(max_length=4)
    billing_address = models.CharField(max_length=50)
    billing_city = models.CharField(max_length=50)
    billing_state = models.CharField(max_length=2, blank=True, null=True)
    billing_zip = models.CharField(max_length=5, blank=True, null=True)
    sign_file = models.ImageField(blank=True, null=True, upload_to=upload_to_cc)

    def __str__(self):
        return self.card_number
