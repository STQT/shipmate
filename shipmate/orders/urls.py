from django.urls import path
from .views import (
    ListOrderAPIView,
    CreateOrderAPIView,
    UpdateOrderAPIView,
    DeleteOrderAPIView,
    DetailOrderAPIView,
    ArchiveListOrderAPIView,
    CreateVehicleOrderAPIView,
    RetrieveUpdateDestroyVehicleOrderAPIView
)

urlpatterns = [
    path('', ListOrderAPIView.as_view(), name='order-list'),
    path('archive/list/', ArchiveListOrderAPIView.as_view(), name='order-archive-list'),
    path('create/', CreateOrderAPIView.as_view(), name='order-create'),

    path('vehicle/add/', CreateVehicleOrderAPIView.as_view(), name='order-add-vehicle'),
    path('vehicle/<int:pk>/', RetrieveUpdateDestroyVehicleOrderAPIView.as_view(),
         name='order-add-vehicle'),

    path('update/<str:guid>/', UpdateOrderAPIView.as_view(), name='order-update'),
    path('detail/<str:guid>/', DetailOrderAPIView.as_view(), name='order-detail'),
    path('delete/<str:guid>/', DeleteOrderAPIView.as_view(), name='order-delete'),
]
