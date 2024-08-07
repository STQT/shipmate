# Generated by Django 4.2.9 on 2024-05-20 12:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("orders", "0005_order_buyer_number_order_cd_note_order_cm_note_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="extra_user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="order_extra_user",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="user",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="order_user",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
