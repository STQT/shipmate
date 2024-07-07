import json
import logging

from django.core.management.base import BaseCommand
from shipmate.addresses.models import City

from geopy.geocoders import Nominatim


def get_coordinates(zipcode=None, city=None, country='US'):
    logging.info(f"Processing: zipcode={zipcode}, city={city}, country={country}")
    geolocator = Nominatim(user_agent="shipmate")

    if not zipcode and not city:
        logging.error("Either zipcode or city must be provided")
        return None, None

    query = {}
    if zipcode:
        query['postalcode'] = zipcode
    if city:
        query['city'] = city
    query['country'] = country

    try:
        location = geolocator.geocode(query)
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

    def handle(self, *args, **options):
        try:
            cities = City.objects.all()
            for num, city in enumerate(cities):
                logging.info(num)
                latitude, longitude = get_coordinates(zipcode=city.zip, city=city.name)
                # Process each item and save to your model
                city.lat = latitude
                city.long = longitude
                city.save()

                self.stdout.write(self.style.SUCCESS('Data imported successfully'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('File not found'))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Invalid JSON format'))
        except Exception as e:
            self.stdout.write(self.style.ERROR('An error occurred: %s' % str(e)))
