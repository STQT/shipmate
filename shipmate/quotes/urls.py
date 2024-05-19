from django.urls import path
from .views import (
    ListQuoteAPIView,
    CreateQuoteAPIView,
    UpdateQuoteAPIView,
    DeleteQuoteAPIView,
    DetailQuoteAPIView,
    ArchiveListQuoteAPIView,
    CreateVehicleLeadsAPIView,
    RetrieveUpdateDestroyVehicleLeadsAPIView
)

urlpatterns = [
    path('', ListQuoteAPIView.as_view(), name='quote-list'),
    path('archive/list/', ArchiveListQuoteAPIView.as_view(), name='quote-archive-list'),
    path('create/', CreateQuoteAPIView.as_view(), name='quote-create'),

    path('vehicle/add/', CreateVehicleLeadsAPIView.as_view(), name='leads-add-vehicle'),
    path('vehicle/<int:pk>/', RetrieveUpdateDestroyVehicleLeadsAPIView.as_view(),
         name='leads-add-vehicle'),

    path('update/<str:guid>/', UpdateQuoteAPIView.as_view(), name='quote-update'),
    path('detail/<str:guid>/', DetailQuoteAPIView.as_view(), name='quote-detail'),
    path('delete/<str:guid>/', DeleteQuoteAPIView.as_view(), name='quote-delete'),
]
