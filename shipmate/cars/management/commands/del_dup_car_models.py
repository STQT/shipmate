# your_app/management/commands/delete_duplicates.py

from django.core.management.base import BaseCommand
from shipmate.cars.models import CarsModel


class Command(BaseCommand):
    help = 'Delete duplicate CarsModel entries'

    def handle(self, *args, **kwargs):
        cars = CarsModel.objects.all().reverse()
        for car in cars:
            count = CarsModel.objects.filter(mark=car.mark, name=car.name, vehicle_type=car.vehicle_type).count()
            if count > 1:
                car.delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted duplicate entries'))
