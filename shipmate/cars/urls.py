from django.urls import path
from .views import (
    ListCarMarksAPIView,
    ListCarsModelAPIView,
    UpdateRetrieveDestroyCarsModelAPIView,
    CreateCarsModelAPIView,
    UpdateRetrieveDestroyCarMarksAPIView,
    CreateCarMarksAPIView
)

urlpatterns = [
    path('marks-list/', ListCarMarksAPIView.as_view(), name='car-marks-list'),
    path('marks/<int:pk>/', UpdateRetrieveDestroyCarMarksAPIView.as_view(), name='car-marks-rud'),
    path('marks/create/', CreateCarMarksAPIView.as_view(), name='car-marks-create'),
    path('models-list/', ListCarsModelAPIView.as_view(), name='car-models-list'),
    path('models/<int:pk>/', UpdateRetrieveDestroyCarsModelAPIView.as_view(), name='car-models-rud'),
    path('models/create/', CreateCarsModelAPIView.as_view(), name='car-models-create'),
]
