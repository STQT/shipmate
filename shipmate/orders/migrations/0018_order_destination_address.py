# Generated by Django 4.2.9 on 2024-06-13 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0017_order_origin_address"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="destination_address",
            field=models.CharField(default="Destination Address", max_length=255),
            preserve_default=False,
        ),
    ]
