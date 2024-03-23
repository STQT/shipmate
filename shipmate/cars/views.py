from rest_framework.generics import ListAPIView

from .models import CarsModel, CarMarks
from .serializers import CarsModelSerializer, CarMarksSerializer


class ListCarsModelAPIView(ListAPIView):
    queryset = CarsModel.objects.all()
    serializer_class = CarsModelSerializer
    filterset_fields = ["mark"]


class ListCarMarksAPIView(ListAPIView):
    queryset = CarMarks.objects.all()
    serializer_class = CarMarksSerializer
