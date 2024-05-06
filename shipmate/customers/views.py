from .filters import CustomerFilter
from .models import Customer, ExternalContacts
from .serializers import CustomerSerializer, ExternalContactsSerializer, DetailCustomerSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, CreateAPIView

from shipmate.contrib.generics import UpdatePUTAPIView


class ListCustomerAPIView(ListAPIView):
    queryset = Customer.objects.prefetch_related("extra")
    serializer_class = DetailCustomerSerializer
    filterset_class = CustomerFilter


class UpdateCustomerAPIView(UpdatePUTAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CreateCustomerAPIView(CreateAPIView):  # noqa
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class DeleteCustomerAPIView(DestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class DetailCustomerAPIView(RetrieveAPIView):
    queryset = Customer.objects.prefetch_related("extra")
    serializer_class = DetailCustomerSerializer


class CreateExternalContactsAPIView(CreateAPIView):  # noqa
    queryset = ExternalContacts.objects.all()
    serializer_class = ExternalContactsSerializer
