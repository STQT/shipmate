# Generated by Django 4.2.9 on 2024-07-07 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0022_alter_order_price_alter_order_reservation_price"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="payment_carrier_pay",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name="order",
            name="payment_cod_to_carrier",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name="order",
            name="payment_paid_reservation",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name="order",
            name="payment_paid_to_carrier",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name="order",
            name="payment_reservation",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name="order",
            name="payment_total_tariff",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]