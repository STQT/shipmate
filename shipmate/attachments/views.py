from django.db import transaction
from rest_framework.generics import CreateAPIView

from shipmate.contrib.models import Attachments
from shipmate.attachments.methods import create_attachment
from ..attachments.serializers import (
    TaskAttachmentSerializer,
    EmailAttachmentSerializer,
    PhoneAttachmentSerializer,
    FileAttachmentSerializer,
    AttachmentType
)
from ..leads.models import LeadsAttachment
from ..orders.models import OrderAttachment
from ..quotes.models import QuoteAttachment


class BaseAttachmentAPIView(CreateAPIView):
    attachment_type = Attachments.TypesChoices.TASK

    @transaction.atomic
    def perform_create(self, serializer):
        rel = serializer.validated_data.pop('rel')
        endpoint_type = serializer.validated_data.pop('endpoint_type')
        attachment_class_map = {
            AttachmentType.QUOTE.value: QuoteAttachment,
            AttachmentType.LEAD.value: LeadsAttachment,
            AttachmentType.ORDER.value: OrderAttachment
        }
        field_map = {
            AttachmentType.QUOTE.value: "quote_id",
            AttachmentType.LEAD.value: "lead_id",
            AttachmentType.ORDER.value: "order_id"
        }
        # Create the TaskAttachment instance
        task_attachment_instance = serializer.save()
        create_attachment(
            task_attachment_instance,
            attachment_class_map[endpoint_type],
            {
                field_map[endpoint_type]: int(rel),
                "type": self.attachment_type,
                "link": task_attachment_instance.id,
            }
        )


class CreateTaskAttachmentAPIView(BaseAttachmentAPIView):
    serializer_class = TaskAttachmentSerializer
    attachment_type = Attachments.TypesChoices.TASK


class CreatePhoneAttachmentAPIView(BaseAttachmentAPIView):
    serializer_class = PhoneAttachmentSerializer
    attachment_type = Attachments.TypesChoices.PHONE


class CreateEmailAttachmentAPIView(BaseAttachmentAPIView):
    serializer_class = EmailAttachmentSerializer
    attachment_type = Attachments.TypesChoices.EMAIL


class CreateFileAttachmentAPIView(BaseAttachmentAPIView):
    serializer_class = FileAttachmentSerializer
    attachment_type = Attachments.TypesChoices.FILE
