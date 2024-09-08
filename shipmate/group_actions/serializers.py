from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.contrib.auth import get_user_model

from shipmate.contrib.models import Attachments, LeadsStatusChoices
from shipmate.group_actions.utils import AttachmentType, ATTACHMENT_FK_FIELD_MAP, ATTACHMENT_CLASS_MAP, \
    ATTACHMENT_ATTACHMENT_MAP
from shipmate.leads.models import Leads
from shipmate.group_actions.tasks import send_sms_task, send_email_task

User = get_user_model()


class GroupArchiveSerializer(serializers.Serializer):
    endpoint_type = serializers.ChoiceField(choices=[(tag.value, tag.name.title()) for tag in AttachmentType],
                                            write_only=True, required=False, allow_null=True)
    ids = serializers.ListField(child=serializers.IntegerField())
    reason = serializers.CharField()

    @transaction.atomic
    def create(self, validated_data):
        ids = validated_data['ids'] # noqa
        endpoint_type = validated_data['endpoint_type']
        reason = validated_data['reason']

        user = self.context['request'].user
        model_class = ATTACHMENT_CLASS_MAP[endpoint_type] # noqa
        fk_field = ATTACHMENT_FK_FIELD_MAP[endpoint_type]
        attachment_class = ATTACHMENT_ATTACHMENT_MAP[endpoint_type]

        if not model_class or not fk_field or not attachment_class:
            raise serializers.ValidationError("Invalid endpoint type")

        objs = model_class.objects.filter(id__in=ids)
        if not objs.exists():
            raise serializers.ValidationError({fk_field: [f"{fk_field.capitalize()} not found"]})

        attachment_objects = []
        for obj in objs:
            data = {
                fk_field: obj,
                "title": f'Archived by {user.first_name} {user.last_name}',
                "user": user,
                "second_title": f'Reason: {reason}',
                "type": Attachments.TypesChoices.ACTIVITY,
                "link": 0
            }
            attachment_objects.append(attachment_class(**data))
        objs.update(status=LeadsStatusChoices.ARCHIVED)
        attachment_class.objects.bulk_create(attachment_objects)
        return validated_data


class GroupReassignSerializer(serializers.Serializer):
    endpoint_type = serializers.ChoiceField(choices=[(tag.value, tag.name.title()) for tag in AttachmentType],
                                            write_only=True, required=False, allow_null=True)
    ids = serializers.ListField(child=serializers.IntegerField())
    user = serializers.IntegerField()
    reason = serializers.CharField()

    def validate_user(self, value):
        get_object_or_404(User, pk=value)
        return value

    @transaction.atomic
    def create(self, validated_data):
        ids = validated_data['ids']
        endpoint_type = validated_data['endpoint_type']
        reason = validated_data['reason']

        user = self.context['request'].user
        extra_user = validated_data['user']

        model_class = ATTACHMENT_CLASS_MAP[endpoint_type]
        fk_field = ATTACHMENT_FK_FIELD_MAP[endpoint_type]
        attachment_class = ATTACHMENT_ATTACHMENT_MAP[endpoint_type]

        if not model_class or not fk_field or not attachment_class:
            raise serializers.ValidationError("Invalid endpoint type")

        objs = model_class.objects.filter(id__in=ids)
        if not objs.exists():
            raise serializers.ValidationError({fk_field: [f"{fk_field.capitalize()} not found"]})

        attachment_objects = []
        for obj in objs:
            data = {
                fk_field: obj,
                "title": f'Reassigned to {user.first_name} {user.last_name}',
                "user": user,
                "second_title": f'Reason: {reason}',
                "type": Attachments.TypesChoices.ACTIVITY,
                "link": 0
            }
            attachment_objects.append(attachment_class(**data))
        objs.update(user_id=extra_user)
        attachment_class.objects.bulk_create(attachment_objects)
        return validated_data


class GroupSMSSerializer(serializers.Serializer):
    endpoint_type = serializers.ChoiceField(choices=[(tag.value, tag.name.title()) for tag in AttachmentType],
                                            write_only=True, required=False, allow_null=True)
    ids = serializers.ListField(child=serializers.IntegerField())
    message = serializers.CharField()

    def create(self, validated_data):
        ids = validated_data['ids']
        endpoint_type = validated_data['endpoint_type']
        message = validated_data['message']  # noqa
        user = self.context['request'].user
        model_class: Leads = ATTACHMENT_CLASS_MAP[endpoint_type]
        fk_field = ATTACHMENT_FK_FIELD_MAP[endpoint_type]
        attachment_class = ATTACHMENT_ATTACHMENT_MAP[endpoint_type]

        if not model_class or not fk_field or not attachment_class:
            raise serializers.ValidationError("Invalid endpoint type")

        objs = model_class.objects.filter(id__in=ids)
        if not objs.exists():
            raise serializers.ValidationError({fk_field: [f"{fk_field.capitalize()} not found"]})
        send_sms_task.delay(user.pk, ids, endpoint_type, message)
        print('check 1')
        # send_sms_task.apply_async(args=(user.pk, ids, endpoint_type, message), countdown=5)
        return validated_data


class GroupEmailSerializer(serializers.Serializer):
    endpoint_type = serializers.ChoiceField(choices=[(tag.value, tag.name.title()) for tag in AttachmentType],
                                            write_only=True, required=False, allow_null=True)
    ids = serializers.ListField(child=serializers.IntegerField())
    subject = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    bcc_list = serializers.ListField(child=serializers.CharField(), required=False, allow_null=True, allow_empty=True)
    cc_list = serializers.ListField(child=serializers.CharField(), required=False, allow_null=True, allow_empty=True)
    message = serializers.CharField()

    def create(self, validated_data):
        ids = validated_data['ids']  # noqa
        endpoint_type = validated_data['endpoint_type']
        subject = validated_data.get("subject", "")
        cc_list = validated_data.get("cc_list", None)
        bcc_list = validated_data.get("bcc_list", None)
        message = validated_data['message']  # noqa
        user = self.context['request'].user
        model_class: Leads = ATTACHMENT_CLASS_MAP[endpoint_type]
        fk_field = ATTACHMENT_FK_FIELD_MAP[endpoint_type]
        attachment_class = ATTACHMENT_ATTACHMENT_MAP[endpoint_type]

        if not model_class or not fk_field or not attachment_class:
            raise serializers.ValidationError("Invalid endpoint type")

        objs = model_class.objects.filter(id__in=ids)
        if not objs.exists():
            raise serializers.ValidationError({fk_field: [f"{fk_field.capitalize()} not found"]})
        send_email_task.delay(user.pk, ids, endpoint_type, message, subject, cc_list, bcc_list)
        return validated_data
