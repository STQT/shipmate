# Generated by Django 4.2.9 on 2024-03-22 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quotes", "0010_auto_20240321_1410"),
    ]

    operations = [
        migrations.AddField(
            model_name="quote",
            name="notes",
            field=models.TextField(blank=True),
        ),
    ]
