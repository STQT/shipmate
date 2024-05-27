from rest_framework import serializers
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

    class Meta:
        model = Role
        fields = ('id', 'access_name', 'access_status', 'included_features', 'access_users')


class RoleSerializer(serializers.ModelSerializer):
    access_users = RoleUserSerializer(many=True, read_only=True)

    class Meta:
        model = Role
        exclude = ["included_features"]


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
            'is_superuser': {'read_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


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
