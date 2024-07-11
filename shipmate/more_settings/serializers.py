from django.contrib.auth import get_user_model
from rest_framework import serializers

from shipmate.more_settings.models import Automation

User = get_user_model()


class AutomationUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.EmailField(read_only=True)


class LogSerializer(serializers.Serializer):
    title = serializers.CharField()
    message = serializers.CharField(allow_null=True)


class RetrieveAutomationSerializer(serializers.ModelSerializer):
    email_template_name = serializers.SerializerMethodField(allow_null=True, read_only=True)
    sms_template_name = serializers.SerializerMethodField(allow_null=True, read_only=True)
    included_users = AutomationUserSerializer(many=True)
    available_users = serializers.SerializerMethodField(read_only=True)
    logs = LogSerializer(many=True)

    class Meta:
        model = Automation
        fields = "__all__"


    def get_email_template_name(self, obj) -> str:
        return obj.email_template.name if obj.email_template else None

    def get_sms_template_name(self, obj) -> str:
        return obj.sms_template.name if obj.sms_template else None

    def get_available_users(self, obj) -> AutomationUserSerializer(many=True):
        included_users = obj.included_users.all()
        users = User.objects.exclude(id__in=included_users.values_list('id', flat=True))
        return AutomationUserSerializer(users, many=True).data


class AutomationSerializer(serializers.ModelSerializer):
    email_template_name = serializers.SerializerMethodField(allow_null=True, read_only=True)
    sms_template_name = serializers.SerializerMethodField(allow_null=True, read_only=True)

    class Meta:
        model = Automation
        fields = "__all__"

    def get_email_template_name(self, obj) -> str:
        return obj.email_template.name if obj.email_template else None

    def get_sms_template_name(self, obj) -> str:
        return obj.sms_template.name if obj.sms_template else None


class CreateAutomationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Automation
        fields = "__all__"


class UpdateAutomationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Automation
        fields = "__all__"
