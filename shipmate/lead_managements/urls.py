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
    path('', ListProviderAPIView.as_view(), name='provider-list'),
    path('create/', CreateProviderAPIView.as_view(), name='provider-create'),
    path('update/<int:pk>/', UpdateProviderAPIView.as_view(), name='provider-update'),
    path('detail/<int:pk>/', DetailProviderAPIView.as_view(), name='provider-detail'),
    path('delete/<int:pk>/', DeleteProviderAPIView.as_view(), name='provider-delete'),

    path('distribution/', ListDistributionAPIView.as_view(), name='distribution-list'),
    path('distribution/update/<int:pk>/', UpdateDistributionAPIView.as_view(), name='distribution-update'),
    path('distribution/detail/<int:pk>/', DetailDistributionAPIView.as_view(), name='distribution-detail'),
]
