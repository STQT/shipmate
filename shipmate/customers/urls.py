from django.urls import path
from .views import ListCustomerAPIView, CreateExternalContactsAPIView
from .views import (
    CreateCustomerAPIView,
    UpdateCustomerAPIView,
    DetailCustomerAPIView,
    DeleteCustomerAPIView
)

urlpatterns = [
    path('', ListCustomerAPIView.as_view(), name='customer-list'),
    path('create-contact/', CreateExternalContactsAPIView.as_view(), name='contact-create'),
    path('create/', CreateCustomerAPIView.as_view(), name='customer-create'),
    path('update/<int:pk>/', UpdateCustomerAPIView.as_view(), name='customer-update'),
    path('detail/<int:pk>/', DetailCustomerAPIView.as_view(), name='customer-detail'),
    path('delete/<int:pk>/', DeleteCustomerAPIView.as_view(), name='customer-delete'),
]
