from django.urls import path
from .views import (
    ListOrderPaymentView, CreateOrderPaymentAPIView,
)

urlpatterns = [
    path('list/<uuid:order>/', ListOrderPaymentView.as_view(),
         name='order-contract-list'),
    path('create/', CreateOrderPaymentAPIView.as_view(),
         name='order-contract-create'),
]
