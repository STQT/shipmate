# Generated by Django 4.2.9 on 2024-05-22 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0007_alter_order_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="location_type",
            field=models.CharField(
                choices=[
                    ("r2r", "Residential to residential"),
                    ("r2b", "Residential to business"),
                    ("b2r", "Business to residential"),
                    ("b2b", "Business to business"),
                ],
                default="b2b",
                max_length=3,
            ),
            preserve_default=False,
        ),
    ]
