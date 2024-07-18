from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from shipmate.group_actions.serializers import GroupReassignSerializer


class GroupReassignView(CreateAPIView):
    serializer_class = GroupReassignSerializer
    permission_classes = [IsAuthenticated]
