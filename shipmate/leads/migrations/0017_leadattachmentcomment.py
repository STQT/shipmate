# Generated by Django 4.2.9 on 2024-06-27 16:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("leads", "0016_leads_updated_from"),
    ]

    operations = [
        migrations.CreateModel(
            name="LeadAttachmentComment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("text", models.TextField()),
                (
                    "attachment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="lead_attachment_comments",
                        to="leads.leadsattachment",
                    ),
                ),
            ],
        ),
    ]