# Generated by Django 4.2.9 on 2024-03-17 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mails", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mail",
            name="date",
            field=models.CharField(max_length=50),
        ),
    ]
