import json
import logging

from django.core.management.base import BaseCommand
from shipmate.addresses.models import City, States

from geopy.geocoders import Nominatim


def get_coordinates(zipcode):
    logging.info(f"Processing: {zipcode}")
    geolocator = Nominatim(user_agent="shipmate")
    try:
        location = geolocator.geocode(zipcode)
        if location:
            latitude = location.latitude
            longitude = location.longitude
            logging.info("FOUND")
            return latitude, longitude
        else:
            logging.warning("Not found")
            return None, None
    except Exception as e:
        logging.error(f"Error: {e}")
        return None, None


class Command(BaseCommand):
    help = 'Import city data from a JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file')

    def handle(self, *args, **options):
        json_file_path = options['json_file']  # noqa

        try:
            with open(json_file_path, 'r') as f:
                data = json.load(f)
                States.objects.all().delete()
                for item in data:
                    fields = item['fields']
                    if item['model'] == "main.states":
                        # Process each item and save to your model
                        states = States(id=item['pk'], name=fields['name']['en'], code=fields['code'])
                        states.save()
                for item in data:
                    if item['model'] == "main.city":
                        fields = item['fields']
                        name = fields['name']['en']
                        latitude, longitude = get_coordinates(fields['zip'])
                        # Process each item and save to your model
                        city = City(
                            state_id=fields['state'],
                            name=name,
                            zip=fields['zip'],
                            long=longitude,
                            lat=latitude
                        )
                        city.save()

                self.stdout.write(self.style.SUCCESS('Data imported successfully'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('File not found'))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Invalid JSON format'))
        except Exception as e:
            self.stdout.write(self.style.ERROR('An error occurred: %s' % str(e)))
