from django.urls import path
from .views import ListCustomerAPIView
from ..leads.views import (
    CreateLeadsAPIView,
    UpdateLeadsAPIView,
    DetailLeadsAPIView,
    DeleteLeadsAPIView
)

urlpatterns = [
    path('customer-list/', ListCustomerAPIView.as_view(), name='customer-list'),
    path('create/', CreateLeadsAPIView.as_view(), name='customer-create'),
    path('<int:pk>/update/', UpdateLeadsAPIView.as_view(), name='customer-update'),
    path('<int:pk>/detail/', DetailLeadsAPIView.as_view(), name='customer-detail'),
    path('<int:pk>/delete/', DeleteLeadsAPIView.as_view(), name='customer-delete'),
]
