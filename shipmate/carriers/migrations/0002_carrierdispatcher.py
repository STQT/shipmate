# Generated by Django 4.2.9 on 2024-05-26 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("carriers", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="CarrierDispatcher",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ],
        ),
    ]