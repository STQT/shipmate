# Generated by Django 4.2.9 on 2024-07-28 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0026_orderattachment_file"),
    ]

    operations = [
        migrations.AddField(
            model_name="ordercontract",
            name="order_data",
            field=models.JSONField(blank=True, null=True),
        ),
    ]