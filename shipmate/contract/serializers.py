from rest_framework import serializers
from .models import Ground, Hawaii, International


class GroundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ground
        exclude = ("updated_from",)

    def validate(self, data):
        instance = self.instance or Ground(**data)
        instance.validate_single_default()
        return data


class HawaiiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hawaii
        exclude = ("updated_from",)

    def validate(self, data):
        instance = self.instance or Hawaii(**data)
        instance.validate_single_default()
        return data


class InternationalSerializer(serializers.ModelSerializer):
    class Meta:
        model = International
        exclude = ("updated_from",)

    def validate(self, data):
        instance = self.instance or International(**data)
        instance.validate_single_default()
        return data
