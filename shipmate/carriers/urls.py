from django.urls import path
from .views import (
    ListCarrierAPIView,
    CreateCarrierAPIView,
    UpdateCarrierAPIView,
    DeleteCarrierAPIView,
    DetailCarrierAPIView,
)

urlpatterns = [
    path('', ListCarrierAPIView.as_view(), name='carrier-list'),
    path('create/', CreateCarrierAPIView.as_view(), name='carrier-create'),

    path('update/<int:pk>/', UpdateCarrierAPIView.as_view(), name='carrier-update'),
    path('detail/<int:pk>/', DetailCarrierAPIView.as_view(), name='carrier-detail'),
    path('delete/<int:pk>/', DeleteCarrierAPIView.as_view(), name='carrier-delete'),

]
