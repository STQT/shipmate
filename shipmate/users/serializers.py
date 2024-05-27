from rest_framework import serializers
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

from shipmate.users.models import User, Feature, Role, Team


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ('id', 'name', 'endpoint', 'method')


class RoleUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.EmailField(read_only=True)


class RetrieveRoleSerializer(serializers.ModelSerializer):
    included_features = FeatureSerializer(many=True, read_only=True)
    access_users = RoleUserSerializer(many=True)
    available_features = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = ('id', 'access_name', 'access_status', 'included_features', 'access_users', 'available_features')

    def get_available_features(self, obj):
        # Retrieve all features from the database
        included_features = obj.included_features.all()
        features = Feature.objects.exclude(id__in=included_features.values_list('id', flat=True))
        # Serialize the features
        return FeatureSerializer(features, many=True).data


class RoleSerializer(serializers.ModelSerializer):
    access_users = RoleUserSerializer(many=True, read_only=True)

    class Meta:
        model = Role
        exclude = ["included_features"]


class CreateRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"


class UpdateRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["is_staff", "groups", "user_permissions"]
        extra_kwargs = {
            'password': {'write_only': True},
            'last_login': {'read_only': True},
            'date_joined': {'read_only': True},
            'is_superuser': {'read_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    newpassword = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        exclude = ["is_staff", "groups", "user_permissions", "password"]
        extra_kwargs = {
            'last_login': {'read_only': True},
            'date_joined': {'read_only': True},
            'is_superuser': {'read_only': True},
        }

    def update(self, instance, validated_data):
        new_password = validated_data.pop('newpassword', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if new_password:
            instance.set_password(new_password)
        instance.save()
        return instance


class UserMeSerializer(serializers.Serializer):
    user = UserSerializer(many=False)
    features = FeatureSerializer(many=True)


class UserEmailResetSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ConfirmOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField()


class ListUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "picture", "first_name", "last_name"]


class ListUserViewSerializer(serializers.ModelSerializer):
    access_role = serializers.SerializerMethodField(allow_null=True)

    def get_access_role(self, obj) -> str:
        return obj.access.access_name if obj.access else "Anonym"

    class Meta:
        model = User
        fields = ["id", "picture", "first_name", "last_name", "email", "created_at",
                  "access_role", "is_active"
                  ]


class TeamSerializer(serializers.ModelSerializer):
    users = ListUserSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = "__all__"
