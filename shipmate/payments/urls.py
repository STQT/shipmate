from django.urls import path
from .views import (
    ListOrderPaymentView, CreateOrderPaymentAPIView, CreateOrderPaymentAttachmentView, ListOrderPaymentAttachmentView,
)

urlpatterns = [
    path('list/<uuid:order>/', ListOrderPaymentView.as_view(),
         name='order-contract-list'),
    path('create/', CreateOrderPaymentAPIView.as_view(),
         name='order-contract-create'),
    path('attachments/', CreateOrderPaymentAttachmentView.as_view(),
         name='order-contract-attachments-create'),
    path('attachments/list/', ListOrderPaymentAttachmentView.as_view(),
         name='order-contract-attachments-list'),
]
