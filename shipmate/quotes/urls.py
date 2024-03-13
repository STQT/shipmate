from django.urls import path
from .views import ListQuoteAPIView, CreateQuoteAPIView, UpdateQuoteAPIView, DeleteQuoteAPIView, DetailQuoteAPIView

urlpatterns = [
    path('quotes/', ListQuoteAPIView.as_view(), name='quote-list'),
    path('quotes/create/', CreateQuoteAPIView.as_view(), name='quote-create'),
    path('quotes/<int:pk>/update/', UpdateQuoteAPIView.as_view(), name='quote-update'),
    path('quotes/<int:pk>/detail/', DetailQuoteAPIView.as_view(), name='quote-detail'),
    path('quotes/<int:pk>/delete/', DeleteQuoteAPIView.as_view(), name='quote-delete'),
]
