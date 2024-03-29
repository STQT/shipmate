from rest_framework.generics import ListAPIView, UpdateAPIView, DestroyAPIView, RetrieveUpdateDestroyAPIView

from .filters import CarMarksFilter, CarsModelFilter
from .models import CarsModel, CarMarks
from .serializers import CarsModelSerializer, CarMarksSerializer


class ListCarsModelAPIView(ListAPIView):
    queryset = CarsModel.objects.all()
    serializer_class = CarsModelSerializer
    filterset_class = CarsModelFilter


class CreateCarsModelAPIView(CreateAPIView):  # noqa
    queryset = CarsModel.objects.all()
    serializer_class = CarsModelSerializer


class UpdateRetrieveDestroyCarsModelAPIView(RetrieveUpdateDestroyAPIView):
    queryset = CarsModel.objects.all()
    serializer_class = CarsModelSerializer


class ListCarMarksAPIView(ListAPIView): # noqa
    queryset = CarMarks.objects.all()
    serializer_class = CarMarksSerializer
    filterset_class = CarMarksFilter


class CreateCarMarksAPIView(CreateAPIView):  # noqa
    queryset = CarMarks.objects.all()
    serializer_class = CarMarksSerializer


class UpdateRetrieveDestroyCarMarksAPIView(RetrieveUpdateDestroyAPIView):
    queryset = CarMarks.objects.all()
    serializer_class = CarMarksSerializer
