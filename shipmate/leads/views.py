from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, CreateAPIView, UpdateAPIView

from shipmate.contrib.models import LeadsStatusChoices
from shipmate.leads.filters import LeadsFilter
from shipmate.leads.models import Leads
from shipmate.leads.serializers import (
    ListLeadsSerializer,
    CreateLeadsSerializer,
    UpdateLeadsSerializer,
    RetrieveLeadsSerializer
)


class ListLeadsAPIView(ListAPIView):
    queryset = Leads.objects.filter(status=LeadsStatusChoices.LEADS)
    serializer_class = ListLeadsSerializer
    filterset_class = LeadsFilter


class CreateLeadsAPIView(CreateAPIView):  # noqa
    queryset = Leads.objects.all()
    serializer_class = CreateLeadsSerializer


class UpdateLeadsAPIView(UpdateAPIView):
    queryset = Leads.objects.all()
    serializer_class = UpdateLeadsSerializer


class DeleteLeadsAPIView(DestroyAPIView):
    queryset = Leads.objects.all()
    serializer_class = CreateLeadsSerializer


class DetailLeadsAPIView(RetrieveAPIView):
    queryset = Leads.objects.all()
    serializer_class = RetrieveLeadsSerializer


class ArchiveListLeadsAPIView(ListAPIView):
    queryset = Leads.objects.filter(status=LeadsStatusChoices.ARCHIVED)
    serializer_class = ListLeadsSerializer
