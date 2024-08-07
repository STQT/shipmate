# Generated by Django 4.2.9 on 2024-03-29 18:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("cars", "0005_alter_carsmodel_vehicle_type"),
        ("leads", "0010_leadsattachment"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="leadsattachment",
            options={"default_related_name": "lead_attachments"},
        ),
        migrations.RemoveField(
            model_name="leads",
            name="vehicle",
        ),
        migrations.RemoveField(
            model_name="leads",
            name="vehicle_year",
        ),
        migrations.CreateModel(
            name="LeadVehicles",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("vehicle_year", models.PositiveSmallIntegerField()),
                ("lead", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="leads.leads")),
                (
                    "vehicle",
                    models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to="cars.carsmodel"),
                ),
            ],
            options={
                "default_related_name": "lead_vehicles",
            },
        ),
    ]
