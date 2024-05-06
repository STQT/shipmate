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
    path('update/<str:guid>/', UpdateQuoteAPIView.as_view(), name='quote-update'),
    path('detail/<str:guid>/', DetailQuoteAPIView.as_view(), name='quote-detail'),
    path('delete/<str:guid>/', DeleteQuoteAPIView.as_view(), name='quote-delete'),
]
