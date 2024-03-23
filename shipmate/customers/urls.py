from django.urls import path
from .views import ListCustomerAPIView, CreateExternalContactsAPIView
from ..leads.views import (
    CreateLeadsAPIView,
    UpdateLeadsAPIView,
    DetailLeadsAPIView,
    DeleteLeadsAPIView
)

urlpatterns = [
    path('', ListCustomerAPIView.as_view(), name='customer-list'),
    path('create-contact/', CreateExternalContactsAPIView.as_view(), name='contact-create'),
    path('create/', CreateLeadsAPIView.as_view(), name='customer-create'),
    path('<int:pk>/update/', UpdateLeadsAPIView.as_view(), name='customer-update'),
    path('<int:pk>/detail/', DetailLeadsAPIView.as_view(), name='customer-detail'),
    path('<int:pk>/delete/', DeleteLeadsAPIView.as_view(), name='customer-delete'),
]
