from rest_framework import serializers

from .models import City, States


class StatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = States
        fields = "__all__"


class CitySerializer(serializers.ModelSerializer):
    state = StatesSerializer(many=False)

    class Meta:
        model = City
        fields = "__all__"
