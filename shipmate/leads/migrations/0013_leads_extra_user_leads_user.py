# Generated by Django 4.2.9 on 2024-05-02 11:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("leads", "0012_alter_leadsattachment_title"),
    ]

    operations = [
        migrations.AddField(
            model_name="leads",
            name="extra_user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="leads_extra_user",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="leads",
            name="user",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="leads_user",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]