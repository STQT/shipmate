from django.urls import path
from .views import (
    CreateNoteAttachmentAPIView,
    CreateTaskAttachmentAPIView, CreateEmailAttachmentAPIView, CreatePhoneAttachmentAPIView,
    CreateFileAttachmentAPIView, ListTaskAttachmentAPIView, CreateTaskAttachmentCommentAPIView,
    TaskAttachmentRetrieveUpdateDestroyAPIView, FileAttachmentRetrieveUpdateDestroyAPIView,
    NoteAttachmentRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path('create-note/', CreateNoteAttachmentAPIView.as_view(), name='create-note'), 
    path('create-task/', CreateTaskAttachmentAPIView.as_view(), name='create-task'),
    path('create-email/', CreateEmailAttachmentAPIView.as_view(), name='create-email'),
    path('create-phone/', CreatePhoneAttachmentAPIView.as_view(), name='create-phone'),
    path('create-file/', CreateFileAttachmentAPIView.as_view(), name='create-file'),
    path('task-list/', ListTaskAttachmentAPIView.as_view(), name='task-list'),
    path('create-task-comment/', CreateTaskAttachmentCommentAPIView.as_view(), name='create-task-comment'),
    path('task/<int:pk>/', TaskAttachmentRetrieveUpdateDestroyAPIView.as_view(),
         name='task_attachment_detail'),
    path('file/<int:pk>/', FileAttachmentRetrieveUpdateDestroyAPIView.as_view(),
         name='file_attachment_detail'),
    path('note/<int:pk>/', NoteAttachmentRetrieveUpdateDestroyAPIView.as_view(),
         name='note_attachment_detail'),
]
