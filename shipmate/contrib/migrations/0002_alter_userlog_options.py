# Generated by Django 4.2.9 on 2024-05-30 12:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("contrib", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="userlog",
            options={"ordering": ["-id"]},
        ),
    ]
