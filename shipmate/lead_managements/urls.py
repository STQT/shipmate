from django.urls import path
from .views import (
    ListDistributionAPIView,
    UpdateDistributionAPIView,
    DetailDistributionAPIView,

    ListProviderAPIView,
    CreateProviderAPIView,
    UpdateProviderAPIView,
    DeleteProviderAPIView,
    DetailProviderAPIView
)

urlpatterns = [
    path('provider/', ListProviderAPIView.as_view(), name='provider-list'),
    path('provider/create/', CreateProviderAPIView.as_view(), name='provider-create'),
    path('provider/update/<int:pk>/', UpdateProviderAPIView.as_view(), name='provider-update'),
    path('provider/detail/<int:pk>/', DetailProviderAPIView.as_view(), name='provider-detail'),
    path('provider/delete/<int:pk>/', DeleteProviderAPIView.as_view(), name='provider-delete'),

    path('distribution/', ListDistributionAPIView.as_view(), name='distribution-list'),
    path('distribution/update/<int:pk>/', UpdateDistributionAPIView.as_view(), name='distribution-update'),
    path('distribution/detail/<int:pk>/', DetailDistributionAPIView.as_view(), name='distribution-detail'),
]
