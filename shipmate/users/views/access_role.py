from rest_framework import generics  # noqa

from shipmate.users.models import Role
from shipmate.users.serializers import (
    RoleSerializer,
)


class RoleCreateAPIView(generics.CreateAPIView):  # noqa
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class RoleDetailAPIView(generics.RetrieveAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class RoleListAPIView(generics.ListAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class RoleUpdateAPIView(generics.UpdateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class RoleDestroyAPIView(generics.DestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
