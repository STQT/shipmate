# Generated by Django 4.2.9 on 2024-09-08 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quotes", "0027_alter_quoteattachment_file"),
    ]

    operations = [
        migrations.AlterField(
            model_name="quoteattachment",
            name="second_title",
            field=models.CharField(blank=True, null=True),
        ),
    ]