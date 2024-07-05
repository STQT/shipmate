from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from shipmate.contrib.models import LeadsStatusChoices, Attachments
from shipmate.contrib.serializers import ArchiveSerializer, ReassignSerializer
from shipmate.leads.models import Leads, LeadsAttachment

User = get_user_model()


class ArchiveView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ArchiveSerializer
    base_class = Leads
    status_choice_class = LeadsStatusChoices
    base_attachment_class = LeadsAttachment
    base_fk_field = "lead"

    def post(self, request, guid):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                obj = self.base_class.objects.get(guid=guid)
            except self.base_class.DoesNotExist:
                return Response({'error': ['Quote not found']}, status=status.HTTP_404_NOT_FOUND)
            reason = serializer.validated_data['reason']  # noqa
            obj.status = LeadsStatusChoices.ARCHIVED
            obj.save()
            data = {
                self.base_fk_field: obj,
                "title": "Archived",
                "user": request.user,
                "second_title": f'Reason: {reason}',
                "type": Attachments.TypesChoices.ACTIVITY,
                "link": 0
            }
            self.base_attachment_class.objects.create(**data)
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReAssignView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReassignSerializer
    base_class = Leads
    base_attachment_class = LeadsAttachment
    base_fk_field = "lead"

    def post(self, request, guid):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                obj = self.base_class.objects.get(guid=guid)
            except self.base_class.DoesNotExist:
                return Response({'guid': [f'{self.base_fk_field.capitalize()} not found']},
                                status=status.HTTP_404_NOT_FOUND)
            extra_user = serializer.validated_data['user']
            extra_user_obj = User.objects.get(pk=extra_user)
            reason = serializer.validated_data['reason']
            # if obj.user == extra_user_obj:
            #     return Response({"user": ["Reasoning user equal to owner"]}, status=status.HTTP_400_BAD_REQUEST)
            obj.user = extra_user_obj
            obj.save()
            data = {
                self.base_fk_field: obj,
                "title": f'Reassigned to {extra_user_obj.first_name} {extra_user_obj.last_name}',
                "user": request.user,
                "second_title": f'Reason: {reason}',
                "type": Attachments.TypesChoices.ACTIVITY,
                "link": 0
            }
            self.base_attachment_class.objects.create(**data)
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
