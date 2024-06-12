from rest_framework import serializers
from .models import Ground, Hawaii, International


class BaseContractSerializer(serializers.ModelSerializer):
    created_by_email = serializers.StringRelatedField(source='created_by.email', read_only=True)
    updated_from_email = serializers.StringRelatedField(source='updated_from.email', read_only=True)

    class Meta:
        model = Ground
        exclude = ("updated_from", 'created_by')


class GroundSerializer(BaseContractSerializer):
    class Meta:
        model = Ground
        exclude = ("updated_from", 'created_by')


class HawaiiSerializer(BaseContractSerializer):
    class Meta:
        model = Hawaii
        exclude = ("updated_from", 'created_by')


class InternationalSerializer(BaseContractSerializer):
    class Meta:
        model = International
        exclude = ("updated_from", 'created_by')
