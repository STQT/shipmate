# Generated by Django 4.2.9 on 2024-03-29 18:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="vehicle",
        ),
        migrations.RemoveField(
            model_name="order",
            name="vehicle_year",
        ),
    ]
