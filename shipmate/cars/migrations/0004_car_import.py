import sys

import requests
from django.db import migrations


def create_mock_data(apps, schema_editor):
    CarMarks = apps.get_model('cars', 'CarMarks')
    makes_response = requests.get('https://carapi.app/api/makes')

    if makes_response.status_code == 200:
        data = makes_response.json()['data']
        for item in data:
            mark_name = item.get('name')
            pk = item.get('id')
            mark, _ = CarMarks.objects.update_or_create(pk=pk, defaults={"name": mark_name})
            sys.stdout.write(f'Successfully created Car: {mark.name}\n')
    else:
        sys.stdout.write('Failed to fetch data from API\n')


def reverse_func(apps, schema_editor):
    # CarMarks = apps.get_model('cars', 'CarMarks')
    # CarMarks.objects.all().delete()
    ...


class Migration(migrations.Migration):
    dependencies = [
        ("cars", "0003_alter_carsmodel_vehicle_type"),
    ]

    operations = [
        # migrations.RunPython(create_mock_data, reverse_func), # FIX: remove for next fix code's
    ]
