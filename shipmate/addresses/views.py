from rest_framework.generics import ListAPIView, CreateAPIView

from shipmate.addresses.filters import CityFilter, StatesFilter
from shipmate.addresses.models import City, States
from shipmate.addresses.serializers import CitySerializer, StatesSerializer, CreateCitySerializer


class CityListAPIView(ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    filterset_class = CityFilter


class CityCreateAPIView(CreateAPIView):
    queryset = City.objects.all()
    serializer_class = CreateCitySerializer


class StatesListAPIView(ListAPIView):
    queryset = States.objects.all()
    serializer_class = StatesSerializer
    filterset_class = StatesFilter
