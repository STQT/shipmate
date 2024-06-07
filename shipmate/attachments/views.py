from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework.generics import CreateAPIView

from shipmate.contrib.models import Attachments
from shipmate.contrib.generics import RetrieveUpdatePUTAPIView
from shipmate.attachments.methods import create_attachment
from .models import TaskAttachment, FileAttachment, NoteAttachment
from ..attachments.serializers import (
    AttachmentType,
    TaskAttachmentSerializer,
    EmailAttachmentSerializer,
    PhoneAttachmentSerializer,
    FileAttachmentSerializer,
    NoteAttachmentSerializer,
    UpdateTaskAttachmentSerializer,
    UpdateFileAttachmentSerializer,
    UpdateNoteAttachmentSerializer
)
from ..leads.models import LeadsAttachment, Leads
from ..orders.models import OrderAttachment, Order
from ..quotes.models import QuoteAttachment, Quote
from rest_framework.exceptions import ValidationError

User = get_user_model()


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
        provider_class_map = {
            AttachmentType.QUOTE.value: Quote,
            AttachmentType.LEAD.value: Leads,
            AttachmentType.ORDER.value: Order
        }
        field_map = {
            AttachmentType.QUOTE.value: "quote_id",
            AttachmentType.LEAD.value: "lead_id",
            AttachmentType.ORDER.value: "order_id"
        }

        # Pre-check if the related object exists
        related_model = attachment_class_map[endpoint_type]  # LeadsAttachment | QuoteAttachment | OrderAttachment
        provider_model = provider_class_map[endpoint_type]  # Leads | Quote | Order
        related_field = field_map[endpoint_type]
        if not provider_model.objects.filter(pk=rel).exists():
            raise ValidationError({"rel": f"The related object: {provider_model.__name__} "
                                          f"with id {rel} does not exist."})

        # Create the TaskAttachment instance
        task_attachment_instance = serializer.save()
        create_attachment(
            task_attachment_instance,
            related_model,
            {
                related_field: int(rel),
                "type": self.attachment_type,
                "link": task_attachment_instance.id,
            }
        )


class CreateTaskAttachmentAPIView(BaseAttachmentAPIView):
    serializer_class = TaskAttachmentSerializer
    attachment_type = Attachments.TypesChoices.TASK


class CreateNoteAttachmentAPIView(BaseAttachmentAPIView):
    serializer_class = NoteAttachmentSerializer
    attachment_type = Attachments.TypesChoices.NOTE


class CreatePhoneAttachmentAPIView(BaseAttachmentAPIView):
    serializer_class = PhoneAttachmentSerializer
    attachment_type = Attachments.TypesChoices.PHONE


class CreateEmailAttachmentAPIView(BaseAttachmentAPIView):
    serializer_class = EmailAttachmentSerializer
    attachment_type = Attachments.TypesChoices.EMAIL

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user if self.request.user.is_authenticated else User.objects.first())


class CreateFileAttachmentAPIView(BaseAttachmentAPIView):
    serializer_class = FileAttachmentSerializer
    attachment_type = Attachments.TypesChoices.FILE


# class TaskAttachmentListAPIView(generics.ListAPIView):
#   TODO: create list view for lead|quote|order id and date filter
#
#     serializer_class = ListTaskAttachmentSerializer
#     queryset = TaskAttachment.objects.all()


class TaskAttachmentRetrieveUpdateDestroyAPIView(RetrieveUpdatePUTAPIView):  # noqa
    queryset = TaskAttachment.objects.all()
    serializer_class = UpdateTaskAttachmentSerializer


class FileAttachmentRetrieveUpdateDestroyAPIView(RetrieveUpdatePUTAPIView):
    queryset = FileAttachment.objects.all()
    serializer_class = UpdateFileAttachmentSerializer


class NoteAttachmentRetrieveUpdateDestroyAPIView(RetrieveUpdatePUTAPIView):
    queryset = NoteAttachment.objects.all()
    serializer_class = UpdateNoteAttachmentSerializer
