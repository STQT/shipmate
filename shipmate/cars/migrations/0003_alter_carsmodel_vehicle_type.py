# Generated by Django 4.2.9 on 2024-03-17 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cars", "0002_alter_carmarks_name_alter_carsmodel_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="carsmodel",
            name="vehicle_type",
            field=models.CharField(
                choices=[
                    ("atv", "ATV"),
                    ("boat", "Boat"),
                    ("car", "Car"),
                    ("heavy", "Heavy equipment"),
                    ("large", "Large Yacht"),
                    ("motorcycle", "Motorcycle"),
                    ("pickup", "Pickup"),
                    ("rv", "RV"),
                    ("suv", "suv"),
                    ("travel", "Travel trailer"),
                    ("van", "Van"),
                    ("other", "Other"),
                ],
                default="Car",
                max_length=255,
                verbose_name="Vehicle type",
            ),
        ),
    ]
