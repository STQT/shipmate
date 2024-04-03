from rest_framework import generics

from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken

from shipmate.users.models import Feature, Role
from shipmate.users.serializers import UserMeSerializer, FeatureSerializer, UserSerializer, RoleSerializer

User = get_user_model()


class UserMeAPIView(generics.RetrieveAPIView):
    serializer_class = UserMeSerializer

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        user_roles = user.roles.prefetch_related('included_features')
        serialized_user = UserSerializer(user).data
        features = []
        for role in user_roles:
            features.extend(role.included_features.all())

        serialized_features = FeatureSerializer(features, many=True).data
        data = {
            'user': serialized_user,
            'features': serialized_features
        }
        return Response(data, status=status.HTTP_200_OK)


class MyTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):  # noqa
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            refresh_token = response.data.get('refresh')
            if refresh_token:
                # Cache the refresh token with a short expiry time
                cache.set(refresh_token, 'valid', timeout=60 * 60 * 24)  # 1 day
        return response


class MyTokenRefreshView(TokenRefreshView):
    ...


class MyTokenVerifyView(TokenVerifyView):
    def post(self, request, *args, **kwargs):
        token = request.data.get('token')
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)
        response = super().post(request, *args, **kwargs)
        # Check if token is in cache
        if cache.get(token):
            return response
        else:
            if response.status_code == status.HTTP_200_OK:
                # Add token to cache with a short expiry time
                cache.set(token, 'valid', timeout=60 * 5)  # 5 minutes
            return response


#       FEATURE
class FeatureCreateAPIView(generics.CreateAPIView): # noqa
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer


class FeatureDetailAPIView(generics.RetrieveAPIView):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer


class FeatureListAPIView(generics.ListAPIView):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer


class FeatureUpdateAPIView(generics.UpdateAPIView):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer


class FeatureDestroyAPIView(generics.DestroyAPIView):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer


#        ROLE
class RoleCreateAPIView(generics.CreateAPIView): # noqa
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
