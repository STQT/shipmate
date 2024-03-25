from django.urls import path
from .views import *

urlpatterns = [
    path('create-task/', CreateTaskAttachmentAPIView.as_view(), name='create-task'),
    path('create-email/', CreateEmailAttachmentAPIView.as_view(), name='create-email'),
    path('create-phone/', CreatePhoneAttachmentAPIView.as_view(), name='create-phone'),
    path('create-file/', CreateFileAttachmentAPIView.as_view(), name='create-file'),
]
