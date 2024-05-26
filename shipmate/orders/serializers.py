from rest_framework import serializers

from .models import Order, OrderVehicles
from ..addresses.serializers import CitySerializer
from ..cars.serializers import CarsModelSerializer
from ..customers.serializers import CustomerSerializer
from ..lead_managements.models import Provider
from ..lead_managements.serializers import ProviderSmallDataSerializer
from ..users.serializers import ListUserSerializer


class CreateVehicleOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderVehicles
        fields = ["vehicle", "vehicle_year", "lot", "vin", "color", "plate"]


class CreateOrderSerializer(serializers.ModelSerializer):
    vehicles = CreateVehicleOrderSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = "__all__"

    def create(self, validated_data):
        vehicles_data = validated_data.pop('vehicles')
        order = Order.objects.create(**validated_data)
        for vehicle_data in vehicles_data:
            OrderVehicles.objects.create(order=order, **vehicle_data)
        return order


class DetailVehicleOrderSerializer(serializers.ModelSerializer):
    vehicle = CarsModelSerializer(many=False)

    class Meta:
        model = OrderVehicles
        fields = "__all__"


class OrderVehicleLeadsSerializer(serializers.ModelSerializer):
    vehicle_name = serializers.SerializerMethodField(read_only=True)  # noqa

    class Meta:
        model = OrderVehicles
        fields = ["vehicle_name"]

    @classmethod
    def get_vehicle_name(cls, obj) -> str:
        vehicle_mark = "NaN"
        vehicle_name = "NaN"
        if obj.vehicle:
            if obj.vehicle.mark:
                vehicle_mark = obj.vehicle.mark.name
            vehicle_name = obj.vehicle.name
        return f"{obj.vehicle_year} {vehicle_mark} {vehicle_name}"


class ListOrderSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()
    customer_phone = serializers.SerializerMethodField()
    origin_name = serializers.SerializerMethodField()
    destination_name = serializers.SerializerMethodField()
    order_vehicles = OrderVehicleLeadsSerializer(many=True)
    user = ListUserSerializer(many=False)
    extra_user = ListUserSerializer(many=False, allow_null=True)

    class Meta:
        model = Order
        fields = "__all__"

    @classmethod
    def get_origin_name(cls, obj) -> str:
        city_name = "NaN"  # noqa
        state_code = "NaN"
        city_zip = "NaN"

        if obj.origin:
            if obj.origin.state:
                city_name = obj.origin.name
                state_code = obj.origin.state.code
            city_zip = obj.origin.zip

        return f"{city_name}, {state_code} {city_zip}"

    @classmethod
    def get_customer_name(cls, obj) -> str:
        return obj.customer.name if obj.customer else "NaN"

    @classmethod
    def get_customer_phone(cls, obj) -> str:
        return obj.customer.phone if obj.customer else "NaN"

    @classmethod
    def get_destination_name(cls, obj) -> str:
        city_name = "NaN"  # noqa
        state_code = "NaN"
        city_zip = "NaN"

        if obj.destination:
            if obj.destination.state:
                city_name = obj.destination.name
                state_code = obj.destination.state.code
            city_zip = obj.destination.zip

        return f"{city_name}, {state_code} {city_zip}"


class RetrieveOrderSerializer(ListOrderSerializer):
    customer = CustomerSerializer(many=False)  # noqa
    origin = CitySerializer(many=False)
    destination = CitySerializer(many=False)
    order_vehicles = DetailVehicleOrderSerializer(many=True)
    source = ProviderSmallDataSerializer(many=False)

    class Meta:
        model = Order
        fields = "__all__"


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class VehicleOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderVehicles
        fields = "__all__"


class ProviderOrderListSerializer(serializers.ModelSerializer):
    order_count = serializers.SerializerMethodField()

    def get_order_count(self, provider) -> int:
        status = self.context['request'].query_params.get('status', None)
        queryset = Order.objects.filter(source=provider)
        if status:
            queryset = queryset.filter(status=status)
        return queryset.count()

    class Meta:
        model = Provider
        fields = ['id', 'name', 'order_count']
