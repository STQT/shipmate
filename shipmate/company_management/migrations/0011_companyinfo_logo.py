# Generated by Django 4.2.9 on 2024-06-12 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("company_management", "0010_add_initial_data"),
    ]

    operations = [
        migrations.AddField(
            model_name="companyinfo",
            name="logo",
            field=models.ImageField(default="logos/image.png", upload_to="logos"),
            preserve_default=False,
        ),
    ]