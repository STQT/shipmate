from rest_framework import serializers

from .models import Customer, ExternalContacts


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


class ExternalContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalContacts
        fields = "__all__"


class SmallExternalContactsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    phone = serializers.CharField()


class DetailCustomerSerializer(serializers.ModelSerializer):
    extra = SmallExternalContactsSerializer(many=True)

    class Meta:
        model = Customer
        fields = "__all__"
