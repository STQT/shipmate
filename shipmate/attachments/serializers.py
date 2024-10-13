import re
from datetime import date
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
from shipmate.contrib.models import Attachments, QuoteStatusChoices
from shipmate.contrib.sms import send_sms
from shipmate.customers.serializers import CustomerSerializer
from shipmate.leads.models import LeadsAttachment, LeadAttachmentComment
from shipmate.orders.models import OrderAttachment, OrderAttachmentComment
from shipmate.quotes.models import QuoteAttachment, QuoteAttachmentComment, Quote
from shipmate.users.serializers import UserSerializer


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
        exclude = ("user",)

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
                    converter_field_name[field_name]: rel,
                    "user_id": self.context['request'].user.id

                }
                try:
                    if field_name == 'quote' and _type == Attachments.TypesChoices.TASK:
                        quote = Quote.objects.get(pk=rel)
                        quote.status = QuoteStatusChoices.UPCOMING
                        quote.save()
                except Exception as e:
                    print(e)
                if _type == Attachments.TypesChoices.FILE:
                    file_url = created_data.file.url if created_data.file else None
                    if file_url:
                        request = self.context['request']
                        url = request.build_absolute_uri('/')[:-1]
                        if 'mate' in url:
                            url = 'https://api.matelogisticss.com'
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
        exclude = ("user",)


class TaskAttachmentSerializer(BaseAttachmentSerializer):
    deadline_string = serializers.SerializerMethodField()  # Add deadline_string field


    class Meta:
        model = TaskAttachment
        fields = ['type', 'priority', 'busy', 'status', 'start_time', 'end_time', 'date', 'deadline_string', 'customer']


    def get_deadline_string(self, obj):
        if not obj.date:
            return None  # If no date is provided, return None

        # Get today's date
        today = date.today()

        # Calculate the difference between the task date and today
        delta = obj.date - today

        # Determine the string based on the delta value
        if delta.days > 1:
            return f"{delta.days} days due"
        elif delta.days == 1:
            return "tomorrow"
        elif delta.days == 0:
            return "today"
        elif delta.days == -1:
            return "1 day past"
        else:
            return f"{abs(delta.days)} days past"


class AttachmentCommentSerializer(serializers.Serializer):
    text = serializers.CharField()


class ListTaskAttachmentSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    customer = CustomerSerializer()
    user = UserSerializer()
    parent = serializers.SerializerMethodField()


    class Meta:
        model = TaskAttachment
        fields = "__all__"

    def get_comments(self, obj):
        from shipmate.attachments.serializers import AttachmentCommentSerializer

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

    def get_parent(self, obj):
        # Try to find the corresponding LeadsAttachment, QuoteAttachment, or OrderAttachment
        attachment = LeadsAttachment.objects.filter(link=obj.pk).first()
        if attachment:
            return {
                'type': 'lead',
                'guid': attachment.lead.guid,
                'id': attachment.lead.id
            }  # Assuming Lead has a guid field

        attachment = QuoteAttachment.objects.filter(link=obj.pk).first()
        if attachment:
            return {
                'type': 'quote',
                'guid': attachment.quote.guid,
                'id': attachment.quote.id
            }  # Assuming Lead has a guid field

        attachment = OrderAttachment.objects.filter(link=obj.pk).first()
        if attachment:
            return {
                'type': 'order',
                'guid': attachment.order.guid,
                'id': attachment.order.id
            }  # Assuming Lead has a guid field

        return None  # Return None if no attachment found



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
        request = self.context.get('request')
        user = request.user if request else None

        to_phone = validated_data.get('to_phone', [])
        text = validated_data.get('text')
        CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

        text = re.sub(CLEANR, '', text)

        if not to_phone:
            raise ValidationError({"to_phone": "At least one recipient phone is required."})

        phone_attachment = super().create(validated_data)
        send_sms(user.phone, to_phone, text)

        return phone_attachment


class EmailAttachmentSerializer(BaseAttachmentSerializer):
    class Meta:
        model = EmailAttachment
        exclude = ('user',)

    def create(self, validated_data):
        to_emails = validated_data.get('to_email', [])
        from_email = validated_data.get('from_email', "leads@matelogisticss.com")
        subject = validated_data.get('subject')
        text = validated_data.get('text', '')
        print(to_emails, from_email, '##########################3')

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
            host='smtp.sendgrid.net',
            user='apikey',
            password=settings.SENDGRID_API_KEY
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
