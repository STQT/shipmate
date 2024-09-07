from rest_framework import serializers
from django.db import models

from .models import Customer, ExternalContacts
from ..contrib.models import OrderStatusChoices
from ..orders.models import Order


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"

    def validate_phone(self, value):
        cleaned_value = value.replace("-", "").replace("(", "").replace(")", "").replace(" ", "")
        return cleaned_value

    def create(self, validated_data):
        validated_data['phone'] = self.validate_phone(validated_data.get('phone', ''))
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['phone'] = self.validate_phone(validated_data.get('phone', instance.phone))
        return super().update(instance, validated_data)


class RetrieveCustomerSerializer(serializers.ModelSerializer):
    phone = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = "__all__"

    @classmethod
    def get_phone(cls, obj) -> str:
        phone = obj.phone if obj.phone else "NaN"
        if phone and len(phone) == 10:  # Assuming phone is a 10-digit number
            return f"({phone[:3]}) {phone[3:6]}-{phone[6:]}"
        return phone


class ExternalContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalContacts
        fields = "__all__"


class SmallExternalContactsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    phone = serializers.CharField()


class DetailCustomerSerializer(serializers.ModelSerializer):
    extra = SmallExternalContactsSerializer(many=True)
    complete = serializers.SerializerMethodField()
    ongoing = serializers.SerializerMethodField()
    uncompleted = serializers.SerializerMethodField()


    class Meta:
        model = Customer
        fields = "__all__"

    @classmethod
    def get_complete(self, obj):
        # Get all related orders and sum the reservation fee (payment_reservation)
        orders = Order.objects.filter(customer_id=obj.id)
        total_reservation_fee = orders.aggregate(total=models.Sum('payment_paid_reservation'))['total']
        return total_reservation_fee or 0  # Return 0 if there are no orders


    @classmethod
    def get_ongoing(self, obj):
        # Define the statuses for ongoing orders
        ongoing_statuses = [
            OrderStatusChoices.ORDERS,
            OrderStatusChoices.BOOKED,
            OrderStatusChoices.POSTED,
            OrderStatusChoices.NOTSIGNED
        ]
        # Filter orders by user and ongoing statuses
        orders = Order.objects.filter(customer_id=obj.id, status__in=ongoing_statuses)
        total_ongoing_reservation = orders.aggregate(total=models.Sum('payment_reservation'))['total']
        return total_ongoing_reservation or 0  # Return 0 if there are no ongoing orders



    @classmethod
    def get_uncompleted(self, obj):
        # Filter orders by user and Archived status
        orders = Order.objects.filter(customer_id=obj.id, status=OrderStatusChoices.ARCHIVED)
        total_uncompleted_reservation = orders.aggregate(total=models.Sum('payment_reservation'))['total']
        return total_uncompleted_reservation or 0  # Return 0 if there are no archived (uncompleted) orders

