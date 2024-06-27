from rest_framework import serializers

from .models import Order, OrderVehicles, OrderAttachment, OrderContract
from ..addresses.serializers import CitySerializer
from ..attachments.serializers import AttachmentCommentSerializer
from ..carriers.models import Carrier
from ..carriers.serializers import CreateCarrierSerializer
from ..cars.serializers import CarsModelSerializer
from ..company_management.models import CompanyInfo
from ..contract.serializers import BaseContractSerializer
from ..customers.serializers import CustomerSerializer
from ..lead_managements.models import Provider
from ..lead_managements.serializers import ProviderSmallDataSerializer
from ..leads.serializers import ListLeadUserSerializer, ListLeadTeamSerializer
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


class DispatchingOrderSerializer(serializers.ModelSerializer):
    carrier_data = CreateCarrierSerializer(source="carrier", many=False, allow_null=True, read_only=True)
    is_dispatch = serializers.BooleanField(required=True, write_only=True)

    class Meta:
        model = Order
        fields = [
            "dispatch_paid_by",
            "dispatch_payment_term",
            "dispatch_term_begins",
            "dispatch_cod_method",
            "dispatch_payment_type",
            "carrier_data",
            "is_dispatch",
        ]
        extra_kwargs = {
            "dispatch_paid_by": {"required": True},
            "dispatch_payment_term": {"required": True},
            "dispatch_term_begins": {"required": True},
            "dispatch_cod_method": {"required": True},
            "dispatch_payment_type": {"required": True},
            "carrier": {"required": True}
        }

    def update(self, instance, validated_data):
        is_dispatch = validated_data.pop('is_dispatch', None)
        if is_dispatch:
            # TODO: Paste here dispatching request
            pass
        instance.save()
        return instance


class DirectDispatchOrderSerializer(serializers.ModelSerializer):
    carrier_data = CreateCarrierSerializer(many=False, write_only=True)
    is_dispatch = serializers.BooleanField(required=True, write_only=True)

    class Meta:
        model = Order
        fields = [
            "dispatch_paid_by", "carrier_data", "is_dispatch",
            "dispatch_payment_term", "dispatch_term_begins", "dispatch_cod_method", "dispatch_payment_type",
            "date_est_pu", "date_est_del", "date_est_ship",
        ]
        extra_kwargs = {
            "dispatch_paid_by": {"required": True},
            "dispatch_payment_term": {"required": True},
            "dispatch_term_begins": {"required": True},
            "dispatch_cod_method": {"required": True},
            "dispatch_payment_type": {"required": True},
            "carrier_data": {"required": True},
        }

    def update(self, instance, validated_data):
        carrier_data = validated_data.pop('carrier_data', None)
        is_dispatch = validated_data.pop('is_dispatch', None)

        carrier = Carrier.objects.create(**carrier_data)
        instance.carrier = carrier
        if is_dispatch:
            # TODO: Paste here dispatching request
            pass
        instance.save()
        return instance


class OrderDatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "date_est_ship",
            "date_est_pu",
            "date_est_del",
            "date_dispatched",
            "date_picked_up",
            "date_delivered",
        ]


class OrderPaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "payment_total_tariff", "payment_reservation", "payment_paid_reservation", "payment_carrier_pay",
            "payment_cod_to_carrier", "payment_paid_to_carrier",
        ]


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
        fields = [
            "id", "guid",
            "customer_name", "customer_phone", "origin_name",
            "destination_name", "order_vehicles", "user", "extra_user",
            "price", "date_est_ship", "condition", "trailer_type", "notes",
            "status",
        ]

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


class OrderContractSerializer(serializers.ModelSerializer):
    executed_on = serializers.SerializerMethodField()

    class Meta:
        model = OrderContract
        fields = "__all__"

    @classmethod
    def get_executed_on(cls, obj) -> str:
        if obj.created_at:
            return obj.created_at.strftime("%m/%d/%Y")
        return "NaN"


class RetrieveOrderSerializer(ListOrderSerializer):
    customer = CustomerSerializer(many=False)  # noqa
    origin = CitySerializer(many=False)
    destination = CitySerializer(many=False)
    order_vehicles = DetailVehicleOrderSerializer(many=True)
    source = ProviderSmallDataSerializer(many=False)
    dispatch_data = DispatchingOrderSerializer(source="*", allow_null=True, required=False)
    dates = OrderDatesSerializer(many=False, source="*")
    payments = OrderPaymentsSerializer(many=False, source="*")

    class Meta:
        model = Order
        exclude = [
            "dispatch_paid_by", "dispatch_payment_term", "dispatch_term_begins", "dispatch_cod_method",
            "dispatch_payment_type", "carrier",
            "date_est_pu", "date_est_del", "date_dispatched", "date_picked_up", "date_delivered",
            "payment_total_tariff", "payment_reservation", "payment_paid_reservation", "payment_carrier_pay",
            "payment_cod_to_carrier", "payment_paid_to_carrier",
        ]


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


class OrderAttachmentSerializer(serializers.ModelSerializer):
    order_attachment_comments = AttachmentCommentSerializer(many=True, read_only=True)

    class Meta:
        model = OrderAttachment
        fields = "__all__"


class CompanyDetailInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyInfo
        fields = "__all__"


class DetailContractSerializer(serializers.Serializer):
    order = RetrieveOrderSerializer(read_only=True)
    contract = OrderContractSerializer(read_only=True)
    company = CompanyDetailInfoSerializer(read_only=True)
    pdf = BaseContractSerializer(read_only=True)


class SigningContractSerializer(serializers.Serializer):
    agreement = serializers.FileField()
    terms = serializers.FileField()


class ListOrdersUserSerializer(ListLeadUserSerializer):
    count = serializers.SerializerMethodField()

    def get_count(self, obj) -> int:
        return Order.objects.filter(user=obj).count()


class ListOrdersTeamSerializer(ListLeadTeamSerializer):
    users = ListOrdersUserSerializer(many=True)
