# Generated by Django 4.2.9 on 2024-08-17 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0027_ordercontract_order_data"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orderattachment",
            name="file",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]