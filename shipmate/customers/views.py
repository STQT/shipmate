from rest_framework.generics import ListAPIView

from .models import Customer
from .serializers import CustomerSerializer


class ListCustomerAPIView(ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

