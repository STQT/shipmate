from rest_framework import serializers

from shipmate.leads.serializers import ListLeadsSerializer
from shipmate.orders.serializers import ListOrderSerializer
from shipmate.quotes.serializers import ListQuoteSerializer


class DataListSerializer(serializers.Serializer):
    key = serializers.CharField()
    value = serializers.CharField()


class BlockListSerializer(serializers.Serializer):
    blockName = serializers.CharField()
    data = DataListSerializer(many=True)


class ModulesListSerializer(serializers.Serializer):
    title = serializers.CharField()
    block = BlockListSerializer(many=True)


class StringListField(serializers.ListField):
    child = serializers.CharField()


class CDPriceSerializer(serializers.Serializer):
    cargo = StringListField()
    route = StringListField()
    price = StringListField()
    accepted = StringListField()
    comparable = StringListField()
    title = serializers.CharField()


class GlobalSearchSerializer(serializers.Serializer):
    leads = ListLeadsSerializer(many=True, allow_empty=True)
    quotes = ListQuoteSerializer(many=True, allow_empty=True)
    orders = ListOrderSerializer(many=True, allow_empty=True)
