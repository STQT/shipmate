# Generated by Django 4.2.9 on 2024-03-24 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("addresses", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="city",
            name="lat",
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="city",
            name="long",
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]
