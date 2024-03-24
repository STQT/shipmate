from django.db import models


class States(models.Model):
    name = models.CharField('State name', max_length=100)
    code = models.CharField('State code', max_length=10)

    def __str__(self):
        return self.name


# cities
class City(models.Model):
    name = models.CharField('Name', max_length=100)
    state = models.ForeignKey(States, on_delete=models.CASCADE, related_name="cities")
    zip = models.CharField('City zip', max_length=5, unique=True)
    text = models.CharField('Text', max_length=100, null=True, blank=True)
    long = models.FloatField(null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} | {self.state.name}"
