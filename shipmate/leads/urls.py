from django.urls import path
from .views import (
    ListLeadsAPIView,
    CreateLeadsAPIView,
    UpdateLeadsAPIView,
    DeleteLeadsAPIView,
    DetailLeadsAPIView, ConvertLeadToQuoteAPIView,
)

urlpatterns = [
    path('', ListLeadsAPIView.as_view(), name='leads-list'),
    path('create/', CreateLeadsAPIView.as_view(), name='leads-create'),
    path('<str:guid>/update/', UpdateLeadsAPIView.as_view(), name='leads-update'),
    path('<str:guid>/detail/', DetailLeadsAPIView.as_view(), name='leads-detail'),
    path('<str:guid>/delete/', DeleteLeadsAPIView.as_view(), name='leads-delete'),
    path('<str:guid>/convert/', ConvertLeadToQuoteAPIView.as_view(), name='leads-to-quote'),
]
