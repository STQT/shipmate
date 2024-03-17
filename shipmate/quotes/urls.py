from django.urls import path
from .views import (
    ListQuoteAPIView,
    CreateQuoteAPIView,
    UpdateQuoteAPIView,
    DeleteQuoteAPIView,
    DetailQuoteAPIView,
    ArchiveListQuoteAPIView
)

urlpatterns = [
    path('', ListQuoteAPIView.as_view(), name='quote-list'),
    path('archive/list/', ArchiveListQuoteAPIView.as_view(), name='quote-archive-list'),
    path('create/', CreateQuoteAPIView.as_view(), name='quote-create'),
    path('<int:pk>/update/', UpdateQuoteAPIView.as_view(), name='quote-update'),
    path('<int:pk>/detail/', DetailQuoteAPIView.as_view(), name='quote-detail'),
    path('<int:pk>/delete/', DeleteQuoteAPIView.as_view(), name='quote-delete'),
]
