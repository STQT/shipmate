# Generated by Django 4.2.9 on 2024-07-15 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0007_alter_orderpaymentcreditcard_sign_file"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderpaymentattachment",
            name="transaction_id",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
