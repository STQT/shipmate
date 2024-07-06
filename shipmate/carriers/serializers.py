from rest_framework import serializers

from shipmate.carriers.models import Carrier


class CreateCarrierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrier
        fields = "__all__"


class ListCarrierSerializer(serializers.ModelSerializer):
    location_name = serializers.SerializerMethodField()
    completed = serializers.IntegerField(default=20)
    ongoing = serializers.IntegerField(default=20)
    price = serializers.IntegerField(default=1200)
    owe = serializers.IntegerField(default=50)

    class Meta:
        model = Carrier
        fields = "__all__"

    @classmethod
    def get_location_name(cls, obj) -> str:
        city_name = "NaN"  # noqa
        state_code = "NaN"
        city_zip = "NaN"

        if obj.location:
            if obj.location.state:
                city_name = obj.location.name
                state_code = obj.location.state.code
            city_zip = obj.location.zip

        return f"{city_name}, {state_code} {city_zip}"


class RetrieveCarrierSerializer(serializers.ModelSerializer):
    # TODO: add columns dynamically calculating orders count

    class Meta:
        model = Carrier
        fields = "__all__"


class UpdateCarrierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrier
        fields = "__all__"
