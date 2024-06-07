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
    rel = serializers.IntegerField(write_only=True)
    endpoint_type = serializers.ChoiceField(choices=[(tag.value, tag.name.title()) for tag in AttachmentType],
                                            write_only=True)

    class Meta:
        model = TaskAttachment
        fields = "__all__"

    def create(self, validated_data):
        rel = validated_data.pop('rel', None)
        text = validated_data.get('text')
        endpoint_type = validated_data.pop('endpoint_type', None)
        created_data = super().create(validated_data)
        if endpoint_type is None:  # noqa
            raise ValidationError({"endpoint_type": "endpointType is required"})
        if isinstance(created_data, NoteAttachment):
            _type = Attachments.TypesChoices.NOTE
        elif isinstance(created_data, FileAttachment):
            _type = Attachments.TypesChoices.FILE
        else:
            _type = Attachments.TypesChoices.TASK
        Class = ATTACHMENT_CLASS_MAP[endpoint_type]  # noqa
        field_name = Class.__name__[:5].lower()
        attachment_class_data = {
            "type": _type,
            "link": created_data.pk,
            "title": strip_tags(text)[:499],
            field_name + "_id": rel
        }
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


class EmailAttachmentSerializer(BaseAttachmentSerializer):
    class Meta:
        model = EmailAttachment
        exclude = ('user',)

    def create(self, validated_data):
        # Extract necessary fields from validated_data
        to_emails = validated_data.get('to_email', [])
        # from_email = validated_data.get('from_email')
        from_email = "gayratbek.sultonov@gmail.com" if settings.DEBUG else "leads@matelogisticss.com"
        subject = validated_data.get('subject')
        text = validated_data.get('text')

        # Validate required fields
        if not to_emails:
            raise ValidationError({"to_email": "At least one recipient email is required."})

        # Create the EmailAttachment instance
        email_attachment = super().create(validated_data)

        # Send the email
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
