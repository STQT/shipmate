# Generated by Django 4.2.9 on 2024-03-21 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Provider",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255)),
                (
                    "status",
                    models.CharField(
                        choices=[("active", "Active"), ("inactive", "Inactive")], default="inactive", max_length=50
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[("standard", "Standard"), ("exclusive", "Exclusive")],
                        default="exclusive",
                        max_length=50,
                    ),
                ),
                ("email", models.EmailField(max_length=254)),
                ("subject", models.CharField(max_length=320)),
                ("is_external", models.BooleanField(default=True)),
            ],
        ),
    ]