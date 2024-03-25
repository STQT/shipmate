from rest_framework import serializers

from shipmate.attachments.models import TaskAttachment, FileAttachment, EmailAttachment, PhoneAttachment
from enum import Enum


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


class TaskAttachmentSerializer(BaseAttachmentSerializer):
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


class FileAttachmentSerializer(BaseAttachmentSerializer):
    class Meta:
        model = FileAttachment
        fields = "__all__"
