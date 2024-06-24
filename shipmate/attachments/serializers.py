from django.db import transaction
from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from shipmate.attachments.models import (
    TaskAttachment,
    FileAttachment,
    EmailAttachment,
    PhoneAttachment,
    NoteAttachment
)
from enum import Enum
from django.utils.html import strip_tags

from shipmate.contrib.email import send_email
from shipmate.contrib.models import Attachments
from shipmate.contrib.sms import send_sms
from shipmate.leads.models import LeadsAttachment
from shipmate.orders.models import OrderAttachment
from shipmate.quotes.models import QuoteAttachment


class AttachmentType(Enum):
    QUOTE = "quote"
    LEAD = "lead"
    ORDER = "order"


ATTACHMENT_CLASS_MAP = {
    AttachmentType.QUOTE.value: QuoteAttachment,
    AttachmentType.LEAD.value: LeadsAttachment,
    AttachmentType.ORDER.value: OrderAttachment
}


class BaseAttachmentSerializer(serializers.ModelSerializer):
    rel = serializers.IntegerField(write_only=True, required=False)
    endpoint_type = serializers.ChoiceField(choices=[(tag.value, tag.name.title()) for tag in AttachmentType],
                                            write_only=True, required=False, allow_null=True)

    class Meta:
        model = TaskAttachment
        fields = "__all__"

    def create(self, validated_data):
        rel = validated_data.pop('rel', None)
        text = validated_data.get('text')
        endpoint_type = validated_data.pop('endpoint_type', None)
        with transaction.atomic():
            created_data = super().create(validated_data)
            if endpoint_type is not None:
                if isinstance(created_data, NoteAttachment):
                    _type = Attachments.TypesChoices.NOTE
                elif isinstance(created_data, FileAttachment):
                    _type = Attachments.TypesChoices.FILE
                else:
                    _type = Attachments.TypesChoices.TASK
                Class = ATTACHMENT_CLASS_MAP[endpoint_type]  # noqa
                field_name = Class.__name__[:5].lower()
                converter_field_name = {
                    "leads": "lead_id",
                    "quote": "quote_id",
                    "order": "order_id"
                }
                attachment_class_data = {
                    "type": _type,
                    "link": created_data.pk,
                    "title": strip_tags(text)[:499],
                    converter_field_name[field_name]: rel
                }
                related_model = Class._meta.get_field(converter_field_name[field_name]).related_model
                if not related_model.objects.filter(pk=rel).exists():
                    raise ValidationError(
                        {
                            converter_field_name[field_name]:
                                f"{converter_field_name[field_name]} with id {rel} does not exist"
                        }
                    )
                Class.objects.create(**attachment_class_data)
        return created_data


class UpdateBaseAttachmentSerializer(serializers.ModelSerializer):
    endpoint_type = serializers.ChoiceField(choices=[(tag.value, tag.name.title()) for tag in AttachmentType],
                                            write_only=True)

    class Meta:
        model = TaskAttachment
        fields = "__all__"

    def update(self, instance, validated_data):
        endpoint_type = validated_data.pop('endpoint_type', None)
        if endpoint_type is None:  # noqa
            raise ValidationError({"endpoint_type": "endpointType is required"})
        if isinstance(instance, NoteAttachment):
            _type = Attachments.TypesChoices.NOTE
        elif isinstance(instance, FileAttachment):
            _type = Attachments.TypesChoices.FILE
        else:
            _type = Attachments.TypesChoices.TASK
        Class = ATTACHMENT_CLASS_MAP[endpoint_type]  # noqa
        attachment = Class.objects.filter(type=_type, link=instance.pk).first()
        if attachment:
            text = validated_data.get('text')
            if text:
                attachment.title = text
                attachment.save()
        return super().update(instance, validated_data)


class NoteAttachmentSerializer(BaseAttachmentSerializer):  # noqa
    class Meta:
        model = NoteAttachment
        fields = "__all__"


class TaskAttachmentSerializer(BaseAttachmentSerializer):
    class Meta:
        model = TaskAttachment
        fields = "__all__"


class ListTaskAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskAttachment
        fields = "__all__"


class PhoneAttachmentSerializer(BaseAttachmentSerializer):
    class Meta:
        model = PhoneAttachment
        fields = "__all__"

    def create(self, validated_data):
        to_phone = validated_data.get('to_phone', [])
        # from_phone = validated_data.get('from_phone')
        # from_phone = "+19294061515"
        # text = validated_data.get('text')

        if not to_phone:
            raise ValidationError({"to_phone": "At least one recipient email is required."})

        email_attachment = super().create(validated_data)
        # send_sms(from_phone, to_phone, text)

        return email_attachment


class EmailAttachmentSerializer(BaseAttachmentSerializer):
    class Meta:
        model = EmailAttachment
        exclude = ('user',)

    def create(self, validated_data):
        to_emails = validated_data.get('to_email', [])
        # from_email = validated_data.get('from_email')
        from_email = "gayratbek.sultonov@gmail.com" if settings.DEBUG else "leads@matelogisticss.com"
        subject = validated_data.get('subject')
        text = validated_data.get('text')

        if not to_emails:
            raise ValidationError({"to_email": "At least one recipient email is required."})

        email_attachment = super().create(validated_data)

        send_email(subject=subject,
                   to_emails=to_emails,
                   from_email=from_email,
                   html_content=text)

        return email_attachment


class FileAttachmentSerializer(BaseAttachmentSerializer):  # noqa
    class Meta:
        model = FileAttachment
        fields = "__all__"


class UpdateNoteAttachmentSerializer(UpdateBaseAttachmentSerializer):
    class Meta:
        model = NoteAttachment
        fields = "__all__"


class UpdateTaskAttachmentSerializer(UpdateBaseAttachmentSerializer):
    class Meta:
        model = TaskAttachment
        fields = "__all__"


class UpdateFileAttachmentSerializer(UpdateBaseAttachmentSerializer):
    class Meta:
        model = FileAttachment
        fields = "__all__"
