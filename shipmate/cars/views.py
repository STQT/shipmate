from rest_framework.generics import ListAPIView, CreateAPIView

from .filters import CarMarksFilter, CarsModelFilter
from .models import CarsModel, CarMarks
from .serializers import CarsModelSerializer, CarMarksSerializer, CreateCarsModelSerializer
from shipmate.contrib.generics import RetrieveUpdatePUTDestroyAPIView


class ListCarsModelAPIView(ListAPIView):  # noqa
    queryset = CarsModel.objects.all()
    serializer_class = CarsModelSerializer
    filterset_class = CarsModelFilter


class CreateCarsModelAPIView(CreateAPIView):  # noqa
    queryset = CarsModel.objects.all()
    serializer_class = CreateCarsModelSerializer


class UpdateRetrieveDestroyCarsModelAPIView(RetrieveUpdatePUTDestroyAPIView):
    queryset = CarsModel.objects.all()
    serializer_class = CarsModelSerializer


class ListCarMarksAPIView(ListAPIView):  # noqa
    queryset = CarMarks.objects.filter(is_active=True)
    serializer_class = CarMarksSerializer
    filterset_class = CarMarksFilter


class CreateCarMarksAPIView(CreateAPIView):  # noqa
    queryset = CarMarks.objects.all()
    serializer_class = CarMarksSerializer


class UpdateRetrieveDestroyCarMarksAPIView(RetrieveUpdatePUTDestroyAPIView):
    queryset = CarMarks.objects.all()
    serializer_class = CarMarksSerializer
