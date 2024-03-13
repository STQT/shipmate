from rest_framework import serializers

from .models import CarsModel, CarMarks


class CarMarksSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarMarks
        fields = "__all__"


class CarsModelSerializer(serializers.ModelSerializer):
    mark = CarMarksSerializer(many=False)

    class Meta:
        model = CarsModel
        fields = "__all__"
