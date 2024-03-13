from rest_framework.generics import ListAPIView

from .models import City, States
from .serializers import CitySerializer, StatesSerializer


class CityListAPIView(ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class StatesListAPIView(ListAPIView):
    queryset = States.objects.all()
    serializer_class = StatesSerializer
