from django.db import models


class CarMarks(models.Model):
    name = models.CharField('Name', max_length=255, blank=True, null=True, db_index=True)
    is_active = models.BooleanField("Is Active?", default=True, db_index=True)

    def __str__(self):
        return self.name


class CarsModel(models.Model):
    class VehicleTYPES(models.TextChoices):
        ATV = "atv", "ATV"
        BOAT = "boat", "Boat"
        CAR = "car", "Car"
        HEAVY = "heavy", "Heavy equipment"
        LARGE = "large", "Large Yacht"
        MOTORCYCLE = "motorcycle", "Motorcycle"
        PICKUP = "pickup", "Pickup"
        RV = 'rv', 'RV'
        SUV = "suv", "suv"
        TRAVEL = 'travel', "Travel trailer"
        VAN = 'van', "Van"
        OTHER = 'other', "Other"

    mark = models.ForeignKey(CarMarks, on_delete=models.CASCADE, related_name='cars')
    name = models.CharField("Name", blank=True, null=True, max_length=255, db_index=True)
    vehicle_type = models.CharField('Vehicle type', max_length=255,
                                    choices=VehicleTYPES.choices, default=VehicleTYPES.CAR)
    is_active = models.BooleanField("Is Active?", default=True, db_index=True)

    def __str__(self):
        return f"{self.mark.name} | {self.name}"
