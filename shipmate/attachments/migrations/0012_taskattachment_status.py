# Generated by Django 4.2.9 on 2024-10-06 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("attachments", "0011_alter_emailattachment_text_alter_fileattachment_text_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="taskattachment",
            name="status",
            field=models.CharField(
                choices=[("support", "Support"), ("completed", "Completed"), ("archived", "Archived")],
                default="support",
                max_length=15,
            ),
        ),
    ]