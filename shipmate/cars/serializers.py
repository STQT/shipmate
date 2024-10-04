from rest_framework import serializers

from .models import CarsModel, CarMarks


class CarMarksSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarMarks
        fields = "__all__"

    # def create(self, validated_data):
    #     # Set is_active to False before saving
    #     validated_data['is_active'] = False
    #     return super().create(validated_data)


class CarsModelSerializer(serializers.ModelSerializer):
    mark = CarMarksSerializer(many=False, read_only=True)

    class Meta:
        model = CarsModel
        fields = "__all__"


class CreateCarsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarsModel
        fields = "__all__"

    # def create(self, validated_data):
    #     # Set is_active to False before saving
    #     validated_data['is_active'] = False
    #     return super().create(validated_data)
