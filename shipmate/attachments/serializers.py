from django.db import transaction
from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from shipmate.attachments.models import (
    TaskAttachment,
    FileAttachment,
    EmailAttachment,
    PhoneAttachment,
    NoteAttachment,
)
from enum import Enum
from django.utils.html import strip_tags

from shipmate.contrib.email import send_email
from shipmate.contrib.models import Attachments
from shipmate.contrib.sms import send_sms
from shipmate.leads.models import LeadsAttachment, LeadAttachmentComment
from shipmate.orders.models import OrderAttachment, OrderAttachmentComment
from shipmate.quotes.models import QuoteAttachment, QuoteAttachmentComment


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
                elif isinstance(created_data, PhoneAttachment):
                    _type = Attachments.TypesChoices.PHONE
                elif isinstance(created_data, EmailAttachment):
                    _type = Attachments.TypesChoices.EMAIL
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
                    "title": text,
                    converter_field_name[field_name]: rel
                }
                if _type == Attachments.TypesChoices.FILE:
                    file_url = created_data.file.url if created_data.file else None
                    if file_url:
                        request = self.context['request']
                        url = request.build_absolute_uri('/')[:-1]
                        attachment_class_data["file"] = f"{url}{file_url}"
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


class AttachmentCommentSerializer(serializers.Serializer):
    text = serializers.CharField()


class ListTaskAttachmentSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()

    class Meta:
        model = TaskAttachment
        fields = "__all__"

    def get_comments(self, obj):
        attachment = LeadsAttachment.objects.filter(link=obj.pk).first()
        rel_name = "lead_attachment_comments"
        if attachment is None:
            attachment = QuoteAttachment.objects.filter(link=obj.pk).first()
            rel_name = "quote_attachment_comments"
            if attachment is None:
                attachment = OrderAttachment.objects.filter(link=obj.pk).first()
                rel_name = "order_attachment_comments"
                if attachment is None:
                    return AttachmentCommentSerializer([], many=True).data
        comments_filter = getattr(attachment, rel_name).all()
        return AttachmentCommentSerializer(comments_filter, many=True).data


class CreateAttachmentCommentSerializer(serializers.Serializer):
    task_id = serializers.IntegerField(write_only=True)
    text = serializers.CharField()

    def create(self, validated_data):
        text = validated_data.get('text')
        task_id = validated_data.pop('task_id', None)
        attachment = LeadsAttachment.objects.filter(link=task_id).first()
        if attachment:
            comment_class = LeadAttachmentComment.objects.create(attachment=attachment, text=text)
        else:
            attachment = QuoteAttachment.objects.filter(link=task_id).first()
            if attachment:
                comment_class = QuoteAttachmentComment.objects.create(attachment=attachment, text=text)
            else:
                attachment = OrderAttachment.objects.filter(link=task_id).first()
                if attachment:
                    comment_class = OrderAttachmentComment.objects.create(attachment=attachment, text=text)
                else:
                    raise ValidationError({"taskId": "Not found Task with taskId"})
        return AttachmentCommentSerializer(comment_class, many=False).data


class PhoneAttachmentSerializer(BaseAttachmentSerializer):
    class Meta:
        model = PhoneAttachment
        fields = "__all__"

    def create(self, validated_data):
        to_phone = validated_data.get('to_phone', [])
        # from_phone = validated_data.get('from_phone')
        from_phone = settings.FROM_PHONE
        text = validated_data.get('text')

        if not to_phone:
            raise ValidationError({"to_phone": "At least one recipient email is required."})

        email_attachment = super().create(validated_data)
        send_sms(from_phone, to_phone, text)

        return email_attachment


class EmailAttachmentSerializer(BaseAttachmentSerializer):
    class Meta:
        model = EmailAttachment
        exclude = ('user',)

    def create(self, validated_data):
        to_emails = validated_data.get('to_email', [])
        from_email = validated_data.get('from_email', "leads@matelogisticss.com")
        subject = validated_data.get('subject')
        text = validated_data.get('text', '')

        if not to_emails:
            raise ValidationError({"to_email": "At least one recipient email is required."})

        email_attachment = super().create(validated_data)

        send_email(
            subject=subject,
            to_emails=to_emails,
            from_email=from_email,
            html_content=text,
            cc_emails=validated_data.get('cc_email', None),
            bcc_emails=validated_data.get('bcc_email', None),
        )

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
