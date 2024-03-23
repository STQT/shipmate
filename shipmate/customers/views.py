from rest_framework.generics import ListAPIView

from .models import Customer
from .serializers import CustomerSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, CreateAPIView, UpdateAPIView


class ListCustomerAPIView(ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CreateCustomerAPIView(CreateAPIView):  # noqa
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class UpdateCustomerAPIView(UpdateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class DeleteCustomerAPIView(DestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class DetailCustomerAPIView(RetrieveAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
