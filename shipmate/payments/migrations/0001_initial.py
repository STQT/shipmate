# Generated by Django 4.2.9 on 2024-07-07 14:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("orders", "0023_alter_order_payment_carrier_pay_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="OrderPayment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "name",
                    models.CharField(
                        choices=[
                            ("auto", "Auto Transportation"),
                            ("auto_carrier", "Auto Transportation (carrier fee)"),
                            ("carrier", "Carrier fee"),
                        ],
                        max_length=12,
                    ),
                ),
                ("quantity", models.PositiveSmallIntegerField()),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("amount_charged", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("discount", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "payment_type",
                    models.CharField(
                        choices=[
                            ("credit", "Credit"),
                            ("card", "Card"),
                            ("zelle", "Zelle"),
                            ("cashapp", "CashApp"),
                            ("venmo", "Venmo"),
                            ("paypal", "PayPal"),
                            ("cash", "Cash"),
                            ("cashier", "Cashier"),
                            ("cashier_check", "Cashier's check"),
                            ("ach", "ACH"),
                        ],
                        max_length=14,
                    ),
                ),
                ("surcharge_fee_rate", models.PositiveSmallIntegerField()),
                (
                    "charge_type",
                    models.CharField(
                        choices=[
                            ("charge", "Charge"),
                            ("refund", "Refund"),
                            ("chargeback", "Chargeback"),
                            ("send", "Send"),
                            ("payroll", "Payroll"),
                        ],
                        max_length=10,
                    ),
                ),
                (
                    "direction",
                    models.CharField(
                        choices=[
                            ("cus2brok", "Customer to Broker"),
                            ("brok2cus", "Broker to Customer"),
                            ("brok2car", "Broker to Carrier"),
                            ("car2brok", "Carrier to Broker"),
                            ("brok2emp", "Broker to Employee"),
                        ],
                        max_length=20,
                    ),
                ),
                ("created_at", models.DateField(auto_now_add=True)),
                (
                    "status",
                    models.CharField(
                        choices=[("created", "Created"), ("paid", "Paid"), ("charge", "Charge")],
                        default="created",
                        max_length=10,
                    ),
                ),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="payments",
                        to="orders.order",
                        to_field="guid",
                    ),
                ),
            ],
        ),
    ]