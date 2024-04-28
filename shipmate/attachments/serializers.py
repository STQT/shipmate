from rest_framework import serializers

from shipmate.attachments.models import (
    TaskAttachment,
    FileAttachment,
    EmailAttachment,
    PhoneAttachment,
    NoteAttachment
)
from enum import Enum

from shipmate.contrib.models import Attachments
from shipmate.leads.models import LeadsAttachment
from shipmate.orders.models import OrderAttachment
from shipmate.quotes.models import QuoteAttachment


class AttachmentType(Enum):
    QUOTE = "quote"
    LEAD = "lead"
    ORDER = "order"


class BaseAttachmentSerializer(serializers.ModelSerializer):
    rel = serializers.IntegerField(write_only=True)
    endpoint_type = serializers.ChoiceField(choices=[(tag.value, tag.name.title()) for tag in AttachmentType],
                                            write_only=True)

    class Meta:
        model = TaskAttachment
        fields = "__all__"


class UpdateBaseAttachmentSerializer(serializers.ModelSerializer):
    endpoint_type = serializers.ChoiceField(choices=[(tag.value, tag.name.title()) for tag in AttachmentType],
                                            write_only=True)

    class Meta:
        model = TaskAttachment
        fields = "__all__"

    def update(self, instance, validated_data):
        endpoint_type = validated_data.pop('endpoint_type', None)
        if endpoint_type:
            attachment_class_map = {
                AttachmentType.QUOTE.value: QuoteAttachment,
                AttachmentType.LEAD.value: LeadsAttachment,
                AttachmentType.ORDER.value: OrderAttachment
            }
        if isinstance(instance, NoteAttachment):
            _type = Attachments.TypesChoices.NOTE
        elif isinstance(instance, FileAttachment):
            _type = Attachments.TypesChoices.FILE
        else:
            _type = Attachments.TypesChoices.TASK
        Class = attachment_class_map[endpoint_type]  # noqa
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
        fields = "__all__"


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
