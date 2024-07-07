from django.db import models


class OrderPayment(models.Model):
    class NameChoices(models.TextChoices):
        auto_transportation = "auto", "Auto Transportation"
        auto_carrier_fee = "auto_carrier", "Auto Transportation (carrier fee)"
        carrier_fee = "carrier", "Carrier fee"

    class TypeChoices(models.TextChoices):
        credit = "credit", "Credit"
        card = "card", "Card"
        zelle = "zelle", "Zelle"
        cashapp = "cashapp", "CashApp"
        venmo = "venmo", "Venmo"
        paypal = "paypal", "PayPal"
        cash = "cash", "Cash"
        cashier = "cashier", "Cashier"
        cashier_check = "cashier_check", "Cashier's check"
        ach = "ach", "ACH"

    class ChargeTypeChoices(models.TextChoices):
        charge = "charge", "Charge"
        refund = "refund", "Refund"
        chargeback = "chargeback", "Chargeback"
        send = "send", "Send"
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
    created_on = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=StatusChoices.choices, default=StatusChoices.CREATED)

    def __str__(self):
        return f"{self.order.pk} | {self.name}"
