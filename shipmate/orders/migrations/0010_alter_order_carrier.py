# Generated by Django 4.2.9 on 2024-05-26 11:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("carriers", "0002_carrierdispatcher"),
        ("orders", "0009_order_carrier"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="carrier",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="orders",
                to="carriers.carrier",
            ),
        ),
    ]