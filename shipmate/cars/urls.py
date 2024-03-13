from django.urls import path
from .views import ListCarMarksAPIView, ListCarsModelAPIView

urlpatterns = [
    path('marks-list/', ListCarMarksAPIView.as_view(), name='car-marks-list'),
    path('models-list/', ListCarsModelAPIView.as_view(), name='car-models-list'),
]
