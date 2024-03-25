from django.db import transaction
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, CreateAPIView, UpdateAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from shipmate.leads.filters import LeadsFilter, LeadsAttachmentFilter
from shipmate.leads.models import Leads, LeadsAttachment
from shipmate.leads.serializers import (
    ListLeadsSerializer,
    CreateLeadsSerializer,
    UpdateLeadsSerializer,
    RetrieveLeadsSerializer, LeadsAttachmentSerializer
)
from shipmate.quotes.models import Quote
from shipmate.quotes.serializers import CreateQuoteSerializer


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


class ConvertLeadToQuoteAPIView(APIView):
    serializer_class = None

    @transaction.atomic
    def post(self, request, guid):
        try:
            lead = Leads.objects.get(guid=guid)
        except Leads.DoesNotExist:
            return Response({"error": "Lead not found"}, status=status.HTTP_404_NOT_FOUND)

        # Convert lead instance to dictionary
        lead_data = lead.__dict__

        # Remove private attributes and Django-related attributes
        lead_data.pop('_state', None)
        lead_data.pop('id', None)
        lead_data.pop('guid', None)

        # Create quote instance using lead fields
        quote_instance = Quote(**lead_data)
        quote_instance.save()

        # Serialize the quote instance
        quote_serializer = CreateQuoteSerializer(quote_instance)
        lead.delete()

        return Response(quote_serializer.data, status=status.HTTP_201_CREATED)


class LeadsAttachmentListView(ListAPIView):
    serializer_class = LeadsAttachmentSerializer
    filterset_class = LeadsAttachmentFilter

    def get_queryset(self):
        lead_id = self.kwargs.get('leadId')  # Retrieve the lead_id from URL kwargs
        return LeadsAttachment.objects.filter(lead_id=lead_id).order_by("-id")
