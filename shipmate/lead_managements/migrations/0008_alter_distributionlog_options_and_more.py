# Generated by Django 4.2.9 on 2024-05-30 12:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("lead_managements", "0007_remove_distribution_is_active_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="distributionlog",
            options={"ordering": ["-id"]},
        ),
        migrations.AlterModelOptions(
            name="providerlog",
            options={"ordering": ["-id"]},
        ),
    ]
