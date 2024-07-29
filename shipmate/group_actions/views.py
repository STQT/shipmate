from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from shipmate.group_actions.serializers import (
    GroupReassignSerializer, GroupSMSSerializer, GroupEmailSerializer, GroupArchiveSerializer
)


class GroupReassignView(CreateAPIView):
    serializer_class = GroupReassignSerializer
    permission_classes = [IsAuthenticated]


class GroupArchiveView(CreateAPIView):
    serializer_class = GroupArchiveSerializer
    permission_classes = [IsAuthenticated]


class GroupSMSSendView(CreateAPIView):
    serializer_class = GroupSMSSerializer
    permission_classes = [IsAuthenticated]


class GroupEmailSendView(CreateAPIView):
    serializer_class = GroupEmailSerializer
    permission_classes = [IsAuthenticated]
