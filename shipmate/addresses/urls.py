from django.urls import path
from .views import CityListAPIView, StatesListAPIView

urlpatterns = [
    path('cities-list/', CityListAPIView.as_view(), name='city-list'),
    path('states-list/', StatesListAPIView.as_view(), name='state-list'),
]
