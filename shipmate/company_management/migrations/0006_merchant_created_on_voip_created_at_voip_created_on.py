# Generated by Django 4.2.9 on 2024-06-06 03:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("company_management", "0005_template_templatelog"),
    ]

    operations = [
        migrations.AddField(
            model_name="merchant",
            name="created_on",
            field=models.ForeignKey(
                default=1,
                editable=False,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="voip",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="voip",
            name="created_on",
            field=models.ForeignKey(
                default=1,
                editable=False,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
