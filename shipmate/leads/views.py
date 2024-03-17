from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, CreateAPIView, UpdateAPIView

from shipmate.leads.models import Leads
from shipmate.leads.serializers import (
    ListLeadsSerializer,
    CreateLeadsSerializer,
    UpdateLeadsSerializer,
    RetrieveLeadsSerializer
)


class ListLeadsAPIView(ListAPIView):
    queryset = Leads.objects.filter(is_archive=False)
    serializer_class = ListLeadsSerializer


class CreateLeadsAPIView(CreateAPIView):
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
    queryset = Leads.objects.filter(is_archive=True)
    serializer_class = ListLeadsSerializer
