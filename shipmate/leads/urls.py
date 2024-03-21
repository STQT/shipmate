from django.urls import path
from .views import (
    ListLeadsAPIView,
    CreateLeadsAPIView,
    UpdateLeadsAPIView,
    DeleteLeadsAPIView,
    DetailLeadsAPIView,
)

urlpatterns = [
    path('', ListLeadsAPIView.as_view(), name='leads-list'),
    path('create/', CreateLeadsAPIView.as_view(), name='leads-create'),
    path('<int:pk>/update/', UpdateLeadsAPIView.as_view(), name='leads-update'),
    path('<int:pk>/detail/', DetailLeadsAPIView.as_view(), name='leads-detail'),
    path('<int:pk>/delete/', DeleteLeadsAPIView.as_view(), name='leads-delete'),
]
