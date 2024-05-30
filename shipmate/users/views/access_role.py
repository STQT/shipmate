from drf_spectacular.utils import extend_schema
from rest_framework import generics  # noqa

from shipmate.contrib.generics import UpdatePUTAPIView
from shipmate.users.filters import RoleFilter
from shipmate.users.models import Role
from shipmate.users.serializers import (
    RoleSerializer, RetrieveRoleSerializer, UpdateRoleSerializer, CreateRoleSerializer,
)

TAG = "users/role/"


@extend_schema(tags=[TAG])  # noqa
class RoleCreateAPIView(generics.CreateAPIView):  # noqa
    queryset = Role.objects.all()
    serializer_class = CreateRoleSerializer


@extend_schema(tags=[TAG])
class RoleDetailAPIView(generics.RetrieveAPIView):
    queryset = Role.objects.prefetch_related("logs")
    serializer_class = RetrieveRoleSerializer


@extend_schema(tags=[TAG])
class RoleListAPIView(generics.ListAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    filterset_class = RoleFilter
    pagination_class = None


@extend_schema(tags=[TAG])
class RoleUpdateAPIView(UpdatePUTAPIView):
    queryset = Role.objects.all()
    serializer_class = UpdateRoleSerializer

    def perform_update(self, serializer):
        serializer.save(updated_from=self.request.user if self.request.user.is_authenticated else None)


@extend_schema(tags=[TAG])  # noqa
class RoleDestroyAPIView(generics.DestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
