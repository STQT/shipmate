# Generated by Django 4.2.9 on 2024-03-17 13:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("leads", "0003_alter_leads_trailer_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="leads",
            name="date_est_ship",
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]