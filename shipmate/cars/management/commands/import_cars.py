import json
from django.core.management.base import BaseCommand
from shipmate.cars.models import CarsModel, CarMarks
from shipmate.contrib.db import update_sequences


class Command(BaseCommand):
    help = 'Import cars data from a JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file')

    def handle(self, *args, **options):
        json_file_path = options['json_file']  # noqa

        try:
            with open(json_file_path, 'r') as f:
                data = json.load(f)
                CarMarks.objects.all().delete()
                for item in data:
                    fields = item['fields']
                    if item['model'] == "main.carmarks":
                        # Process each item and save to your model
                        carmarks = CarMarks(id=item['pk'], name=fields['name']['en'])
                        carmarks.save()
                for item in data:
                    fields = item['fields']
                    if item['model'] == "main.carsmodel":
                        # Process each item and save to your model
                        carsmodel = CarsModel(
                            mark_id=fields['mark'],
                            name=fields['name']['en'],
                            vehicle_type=fields['vehicle_type']
                        )
                        carsmodel.save()

                update_sequences(CarMarks, 'cars_carmarks_id_seq')
                update_sequences(CarsModel, 'cars_carsmodel_id_seq')

                self.stdout.write(self.style.SUCCESS('Data imported successfully'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('File not found'))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Invalid JSON format'))
        except Exception as e:
            self.stdout.write(self.style.ERROR('An error occurred: %s' % str(e)))
