# Generated by Django 4.2.9 on 2024-06-03 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lead_managements", "0009_provider_default_deposit_provider_value"),
    ]

    operations = [
        migrations.AddField(
            model_name="provider",
            name="leads_in_queue",
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]
