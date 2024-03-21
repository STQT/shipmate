from django.urls import path
from .views import (
    ListProviderAPIView,
    CreateProviderAPIView,
    UpdateProviderAPIView,
    DeleteProviderAPIView,
    DetailProviderAPIView
)

urlpatterns = [
    path('', ListProviderAPIView.as_view(), name='provider-list'),
    path('create/', CreateProviderAPIView.as_view(), name='provider-create'),
    path('<int:pk>/update/', UpdateProviderAPIView.as_view(), name='provider-update'),
    path('<int:pk>/detail/', DetailProviderAPIView.as_view(), name='provider-detail'),
    path('<int:pk>/delete/', DeleteProviderAPIView.as_view(), name='provider-delete'),
]
