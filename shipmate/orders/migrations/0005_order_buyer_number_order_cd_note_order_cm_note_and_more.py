# Generated by Django 4.2.9 on 2024-05-20 11:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("cars", "0006_carmarks_is_active_carsmodel_is_active_and_more"),
        ("orders", "0004_remove_order_date_delivered_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="buyer_number",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="order",
            name="cd_note",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="order",
            name="cm_note",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="order",
            name="date_delivered",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="order",
            name="date_dispatched",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="order",
            name="date_est_del",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="order",
            name="date_est_pu",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="order",
            name="date_picked_up",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="order",
            name="destination_business_name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="order",
            name="destination_business_phone",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="order",
            name="destination_contact_person",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="order",
            name="destination_phone",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="order",
            name="destination_second_phone",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="order",
            name="origin_business_name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="order",
            name="origin_business_phone",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="order",
            name="origin_buyer_number",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="order",
            name="origin_contact_person",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="order",
            name="origin_phone",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="order",
            name="origin_second_phone",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="order",
            name="payment_carrier_pay",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="order",
            name="payment_cod_to_carrier",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="order",
            name="payment_paid_reservation",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="order",
            name="payment_paid_to_carrier",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="order",
            name="payment_reservation",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="order",
            name="payment_total_tariff",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="order",
            name="condition",
            field=models.CharField(
                choices=[("run", "Run and drives"), ("rols", "Inop, it rolls")], default="run", max_length=50
            ),
        ),
        migrations.CreateModel(
            name="OrderVehicles",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("vehicle_year", models.PositiveSmallIntegerField()),
                ("lot", models.CharField(blank=True, max_length=20, null=True)),
                ("vin", models.CharField(blank=True, max_length=50, null=True)),
                ("color", models.CharField(blank=True, max_length=100, null=True)),
                ("plate", models.CharField(blank=True, max_length=50, null=True)),
                ("order", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="orders.order")),
                (
                    "vehicle",
                    models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to="cars.carsmodel"),
                ),
            ],
            options={
                "default_related_name": "order_vehicles",
            },
        ),
    ]
