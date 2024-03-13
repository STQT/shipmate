from django.urls import path
from .views import ListCustomerAPIView

urlpatterns = [
    path('customer-list/', ListCustomerAPIView.as_view(), name='customer-list'),
]
