# Generated by Django 4.2.9 on 2024-03-22 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("leads", "0008_auto_20240321_1409"),
    ]

    operations = [
        migrations.AddField(
            model_name="leads",
            name="notes",
            field=models.TextField(blank=True),
        ),
    ]