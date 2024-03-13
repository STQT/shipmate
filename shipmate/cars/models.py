from django.db import models


class CarMarks(models.Model):
    name = models.JSONField('Name', blank=True, null=True)

    def __str__(self):
        return self.name


class CarsModel(models.Model):
    class VehicleTYPES(models.TextChoices):
        CAR = "Car", "car"
        SUV = "SUV", "suv"
        PICKUP = "Pickup", "pickup"

    mark = models.ForeignKey(CarMarks, on_delete=models.CASCADE, related_name='cars')
    name = models.JSONField("Name", blank=True, null=True, max_length=255)
    vehicle_type = models.CharField('Vehicle type', max_length=255,
                                    choices=VehicleTYPES.choices, default='Car')
