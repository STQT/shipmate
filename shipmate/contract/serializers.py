from rest_framework import serializers
from .models import Ground, Hawaii, International


class GroundSerializer(serializers.ModelSerializer):
    created_by_email = serializers.StringRelatedField(source='created_by.email', read_only=True)
    updated_from_email = serializers.StringRelatedField(source='updated_from.email', read_only=True)

    class Meta:
        model = Ground
        exclude = ("updated_from", 'created_by')

    def validate(self, data):
        instance = self.instance or Ground(**data)
        instance.validate_single_default()
        return data


class HawaiiSerializer(serializers.ModelSerializer):
    created_by_email = serializers.StringRelatedField(source='created_by.email', read_only=True)
    updated_from_email = serializers.StringRelatedField(source='updated_from.email', read_only=True)

    class Meta:
        model = Hawaii
        exclude = ("updated_from", 'created_by')

    def validate(self, data):
        instance = self.instance or Hawaii(**data)
        instance.validate_single_default()
        return data


class InternationalSerializer(serializers.ModelSerializer):
    created_by_email = serializers.StringRelatedField(source='created_by.email', read_only=True)
    updated_from_email = serializers.StringRelatedField(source='updated_from.email', read_only=True)

    class Meta:
        model = International
        exclude = ("updated_from", 'created_by')

    def validate(self, data):
        instance = self.instance or International(**data)
        instance.validate_single_default()
        return data
