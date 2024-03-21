from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, CreateAPIView, UpdateAPIView

from shipmate.leads.filters import LeadsFilter
from shipmate.leads.models import Leads
from shipmate.leads.serializers import (
    ListLeadsSerializer,
    CreateLeadsSerializer,
    UpdateLeadsSerializer,
    RetrieveLeadsSerializer
)


class ListLeadsAPIView(ListAPIView):  # noqa
    queryset = Leads.objects.all()
    serializer_class = ListLeadsSerializer
    filterset_class = LeadsFilter
    ordering = ("-id",)


class CreateLeadsAPIView(CreateAPIView):  # noqa
    queryset = Leads.objects.all()
    serializer_class = CreateLeadsSerializer


class UpdateLeadsAPIView(UpdateAPIView):
    queryset = Leads.objects.all()
    serializer_class = UpdateLeadsSerializer
    lookup_field = 'guid'


class DeleteLeadsAPIView(DestroyAPIView):
    queryset = Leads.objects.all()
    serializer_class = CreateLeadsSerializer
    lookup_field = 'guid'


class DetailLeadsAPIView(RetrieveAPIView):
    queryset = Leads.objects.all()
    serializer_class = RetrieveLeadsSerializer
    lookup_field = 'guid'
