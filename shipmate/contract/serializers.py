from rest_framework import serializers
from .models import Ground, Hawaii, International


class GroundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ground
        fields = '__all__'

    def validate(self, data):
        instance = self.instance or Ground(**data)
        instance.validate_single_default()
        return data


class HawaiiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hawaii
        fields = '__all__'

    def validate(self, data):
        instance = self.instance or Hawaii(**data)
        instance.validate_single_default()
        return data


class InternationalSerializer(serializers.ModelSerializer):
    class Meta:
        model = International
        fields = '__all__'

    def validate(self, data):
        instance = self.instance or International(**data)
        instance.validate_single_default()
        return data
