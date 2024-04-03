from rest_framework import serializers
from .models import User, Feature, Role


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ('id', 'name', 'endpoint', 'method')


class RetrieveRoleSerializer(serializers.ModelSerializer):
    included_features = FeatureSerializer(many=True, read_only=True)

    class Meta:
        model = Role
        fields = ('id', 'access_name', 'access_status', 'included_features')  # Add more fields as needed


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email']


class UserMeSerializer(serializers.Serializer):
    user = UserSerializer(many=False)
    features = FeatureSerializer(many=True)
