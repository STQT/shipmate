import random
from django.contrib.auth import get_user_model
from rest_framework import serializers

from shipmate.insights.models import Goal, GoalGroup, LeadsInsight
from shipmate.users.serializers import ListUserSerializer

User = get_user_model()


class GoalGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoalGroup
        fields = "__all__"


class RetrieveGoalSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    group = GoalGroupSerializer(many=False)

    class Meta:
        model = Goal
        fields = "__all__"

    @classmethod
    def get_user_name(cls, obj) -> str:
        user = obj.user
        if not obj.user:
            return "NaN"
        name = user.first_name
        last_name = user.last_name if user.last_name else ""
        return name + " " + last_name


class ListGoalSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    group = GoalGroupSerializer(many=False)
    target_weekly = serializers.SerializerMethodField(allow_null=True, read_only=True)
    actual_week = serializers.SerializerMethodField(allow_null=True, read_only=True)
    target_monthly = serializers.SerializerMethodField(allow_null=True, read_only=True)
    actual_month = serializers.SerializerMethodField(allow_null=True, read_only=True)

    class Meta:
        model = Goal
        fields = "__all__"

    @classmethod
    def get_user_name(cls, obj) -> str:
        user = obj.user
        if not obj.user:
            return "NaN"
        name = user.first_name
        last_name = user.last_name if user.last_name else ""
        return name + " " + last_name

    def get_target_weekly(self, obj) -> float:
        return round(random.uniform(0, 1000), 2)

    def get_actual_week(self, obj) -> float:
        return round(random.uniform(0, 1000), 2)

    def get_target_monthly(self, obj) -> float:
        return round(random.uniform(0, 1000), 2)

    def get_actual_month(self, obj) -> float:
        return round(random.uniform(0, 1000), 2)


class CreateGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = "__all__"


class UpdateGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = "__all__"


# Lead Insight

class ListLeadsInsightUserSerializer(serializers.ModelSerializer):
    user = ListUserSerializer()

    class Meta:
        model = LeadsInsight
        fields = "__all__"
