from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView, ListAPIView

from shipmate.contrib.models import Attachments
from shipmate.contrib.generics import RetrieveUpdatePUTAPIView
from .filters import TaskAttachmentFilter
from .models import TaskAttachment, FileAttachment, NoteAttachment
from ..attachments.serializers import (
    TaskAttachmentSerializer,
    EmailAttachmentSerializer,
    PhoneAttachmentSerializer,
    FileAttachmentSerializer,
    NoteAttachmentSerializer,
    UpdateTaskAttachmentSerializer,
    UpdateFileAttachmentSerializer,
    UpdateNoteAttachmentSerializer,
    ListTaskAttachmentSerializer, CreateAttachmentCommentSerializer
)

User = get_user_model()


class BaseAttachmentAPIView(CreateAPIView):
    attachment_type = Attachments.TypesChoices.TASK

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user if self.request.user.is_authenticated else User.objects.first())


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


class TaskAttachmentRetrieveUpdateDestroyAPIView(RetrieveUpdatePUTAPIView):  # noqa
    queryset = TaskAttachment.objects.all()
    serializer_class = UpdateTaskAttachmentSerializer


class ListTaskAttachmentAPIView(ListAPIView):  # noqa
    queryset = TaskAttachment.objects.all()
    serializer_class = ListTaskAttachmentSerializer
    filterset_class = TaskAttachmentFilter


class CreateTaskAttachmentCommentAPIView(CreateAPIView):  # noqa
    serializer_class = CreateAttachmentCommentSerializer


class FileAttachmentRetrieveUpdateDestroyAPIView(RetrieveUpdatePUTAPIView):
    queryset = FileAttachment.objects.all()
    serializer_class = UpdateFileAttachmentSerializer


class NoteAttachmentRetrieveUpdateDestroyAPIView(RetrieveUpdatePUTAPIView):
    queryset = NoteAttachment.objects.all()
    serializer_class = UpdateNoteAttachmentSerializer
