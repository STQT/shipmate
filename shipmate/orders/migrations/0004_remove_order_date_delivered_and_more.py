# Generated by Django 4.2.9 on 2024-05-13 16:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0003_alter_orderattachment_title"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="date_delivered",
        ),
        migrations.RemoveField(
            model_name="order",
            name="date_dispatched",
        ),
        migrations.RemoveField(
            model_name="order",
            name="date_est_del",
        ),
        migrations.RemoveField(
            model_name="order",
            name="date_est_pu",
        ),
        migrations.RemoveField(
            model_name="order",
            name="date_picked_up",
        ),
        migrations.RemoveField(
            model_name="order",
            name="payment_carrier_pay",
        ),
        migrations.RemoveField(
            model_name="order",
            name="payment_cod_to_carrier",
        ),
        migrations.RemoveField(
            model_name="order",
            name="payment_paid_reservation",
        ),
        migrations.RemoveField(
            model_name="order",
            name="payment_paid_to_carrier",
        ),
        migrations.RemoveField(
            model_name="order",
            name="payment_reservation",
        ),
        migrations.RemoveField(
            model_name="order",
            name="payment_total_tariff",
        ),
    ]