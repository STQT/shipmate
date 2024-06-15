from rest_framework import serializers


class ReassignSerializer(serializers.Serializer):
    user = serializers.IntegerField()
    reason = serializers.CharField()


class ArchiveSerializer(serializers.Serializer):
    reason = serializers.CharField()
