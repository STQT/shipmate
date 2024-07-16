from rest_framework import serializers

from .models import Customer, ExternalContacts


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

    class Meta:
        model = Customer
        fields = "__all__"
