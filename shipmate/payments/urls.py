from django.urls import path
from .views import (
    ListOrderPaymentView, CreateOrderPaymentAPIView, CreateOrderPaymentAttachmentView, ListOrderPaymentAttachmentView,
    ListOrderPaymentCreditCardView, CreateOrderPaymentCreditCardAPIView, CreateOrderCustomerPaymentCreditCardAPIView,
    SendCCAToPaymentView, DetailOrderCustomerContractView, RefundPaymentSerializerView, DetailOrderCustomerPaymentView
)

urlpatterns = [
    path('list/<uuid:order>/', ListOrderPaymentView.as_view(),
         name='order-contract-list'),
    path('create/', CreateOrderPaymentAPIView.as_view(),
         name='order-contract-create'),
    path('send-cca/<int:payment>/', SendCCAToPaymentView.as_view(),
         name='order-cca-send'),
    path('customer/<uuid:order>/', DetailOrderCustomerContractView.as_view(),
         name='contract-payment-detail'),
    path('customer/<uuid:order>/<int:payment_id>/', DetailOrderCustomerPaymentView.as_view(),
         name='order-payment-detail'),
    path('attachments/', CreateOrderPaymentAttachmentView.as_view(),
         name='order-contract-attachments-create'),
    path('refund/', RefundPaymentSerializerView.as_view(),
         name='order-refund-create'),
    path('attachments/list/', ListOrderPaymentAttachmentView.as_view(),
         name='order-contract-attachments-list'),
    path('credit-cards/', ListOrderPaymentCreditCardView.as_view(), name='cc-list'),
    path('credit-cards/customer/create/', CreateOrderCustomerPaymentCreditCardAPIView.as_view(),
         name='cc-customer-create'),
    path('credit-cards/create/', CreateOrderPaymentCreditCardAPIView.as_view(), name='cc-create')
]
