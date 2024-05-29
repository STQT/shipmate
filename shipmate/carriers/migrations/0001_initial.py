from django.db import migrations, models
import django.db.models.deletion


def create_initial_carrier(apps, schema_editor):
    Carrier = apps.get_model("carriers", "Carrier")
    States = apps.get_model("addresses", "States")
    City = apps.get_model("addresses", "City")
    state, _created = States.objects.get_or_create(name='Washington', code="WA")
    city, _created = City.objects.get_or_create(
        name="Unknown", zip="00000", long=0, lat=0, state=state
    )
    initial_carrier = Carrier(
        id=1,
        name="Initial Carrier",
        address="123 Main St",
        mc_number="MC123456",
        contact_name="John Doe",
        phone="123-456-7890",
        phone_2="098-765-4321",
        email="contact@initialcarrier.com",
        fax="123-456-7891",
        status="favorite",
        location=city
    )
    initial_carrier.save()


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("addresses", "0003_alter_city_lat_alter_city_long"),
    ]

    operations = [
        migrations.CreateModel(
            name="Carrier",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255)),
                ("address", models.CharField(max_length=255)),
                ("mc_number", models.CharField(max_length=255)),
                ("contact_name", models.CharField(max_length=255)),
                ("phone", models.CharField(max_length=20)),
                ("phone_2", models.CharField(blank=True, max_length=20, null=True)),
                ("email", models.EmailField(max_length=254)),
                ("fax", models.CharField(max_length=20)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("favorite", "Favorite"),
                            ("active", "Active"),
                            ("inactive", "Inactive"),
                            ("blocked", "Blocked"),
                        ],
                        default="inactive",
                        max_length=8,
                    ),
                ),
                (
                    "location",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="carriers", to="addresses.city"
                    ),
                ),
            ],
            options={
                "verbose_name": "Carrier",
                "verbose_name_plural": "Carriers",
            },
        ),
        migrations.RunPython(create_initial_carrier),
    ]
