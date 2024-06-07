from rest_framework import serializers


class DataListSerializer(serializers.Serializer):
    key = serializers.CharField()
    value = serializers.CharField()


class BlockListSerializer(serializers.Serializer):
    blockName = serializers.CharField()
    data = DataListSerializer(many=True)


class ModulesListSerializer(serializers.Serializer):
    title = serializers.CharField()
    block = BlockListSerializer(many=True)
