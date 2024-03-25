from django.urls import path
from .views import *

urlpatterns = [
    path('create-task/', CreateTaskAttachmentAPIView.as_view(), name='create-task'),
    path('create-email/', CreateEmailAttachmentAPIView.as_view(), name='create-email'),
    path('create-phone/', CreatePhoneAttachmentAPIView.as_view(), name='create-phone'),
    path('create-file/', CreateFileAttachmentAPIView.as_view(), name='create-file'),
    path('task/<int:pk>/', TaskAttachmentRetrieveUpdateDestroyAPIView.as_view(),
         name='task_attachment_detail'),
    path('phone/<int:pk>/', PhoneAttachmentRetrieveUpdateDestroyAPIView.as_view(),
         name='phone_attachment_detail'),
    path('email/<int:pk>/', EmailAttachmentRetrieveUpdateDestroyAPIView.as_view(),
         name='email_attachment_detail'),
    path('file/<int:pk>/', FileAttachmentRetrieveUpdateDestroyAPIView.as_view(),
         name='file_attachment_detail'),
]
