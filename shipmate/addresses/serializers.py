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


class CreateCitySerializer(serializers.ModelSerializer):
    state_code = serializers.CharField(write_only=True, max_length=2)

    class Meta:
        model = City
        fields = ['name', 'zip', 'state_code']

    def validate_state_code(self, value):
        if not States.objects.filter(code=value.upper()).exists():
            raise serializers.ValidationError(f"State with code '{value}' does not exist.")
        return value

    def create(self, validated_data):
        state_code = validated_data.pop('state_code')
        state = States.objects.get(code=state_code.upper())
        city = City.objects.create(state=state, **validated_data)
        return city
