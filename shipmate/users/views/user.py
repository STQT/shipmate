import logging

from django.conf import settings
from drf_spectacular.utils import extend_schema
from rest_framework import generics

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework_simplejwt.tokens import RefreshToken

from shipmate.contrib.generics import UpdatePUTAPIView
from shipmate.users.filters import UserFilter
from shipmate.users.models import OTPCode
from shipmate.users.serializers import (
    UserMeSerializer, FeatureSerializer,
    UserSerializer,
    UserEmailResetSerializer,
    ConfirmOTPSerializer, ChangePasswordSerializer, CreateUserSerializer, ListUserViewSerializer, UpdateUserSerializer,
    DetailUserSerializer
)

User = get_user_model()

TOKEN_TAG = "users/token/"


class UserMeAPIView(generics.RetrieveAPIView):
    serializer_class = UserMeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        serialized_user = UserSerializer(user).data
        serialized_features = []
        user_access = user.access
        if user_access:
            features = user_access.included_features.all()
            serialized_features = FeatureSerializer(features, many=True).data
        data = {
            'user': serialized_user,
            'features': serialized_features
        }
        return Response(data, status=status.HTTP_200_OK)


class UserCreateViewSet(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CreateUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListViewSet(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = None
    serializer_class = ListUserViewSerializer
    queryset = User.objects.all()
    filterset_class = UserFilter


class UserUpdateViewSet(UpdatePUTAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateUserSerializer

    def perform_update(self, serializer):
        serializer.save(updated_from=self.request.user if self.request.user.is_authenticated else None)


class UserDetailViewSet(generics.RetrieveAPIView):
    queryset = User.objects.prefetch_related("logs")
    permission_classes = [IsAuthenticated]
    serializer_class = DetailUserSerializer


@extend_schema(tags=[TOKEN_TAG])
class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):  # noqa
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            refresh_token = response.data.get('refresh')
            if refresh_token:
                # Cache the refresh token with a short expiry time
                cache.set(refresh_token, 'valid', timeout=60 * 60 * 24)  # 1 day
        return response


@extend_schema(tags=[TOKEN_TAG])
class MyTokenRefreshView(TokenRefreshView):
    permission_classes = (AllowAny,)


@extend_schema(tags=[TOKEN_TAG])
class MyTokenVerifyView(TokenVerifyView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        token = request.data.get('token')
        if not token:
            return Response({'token': ['Token is required']}, status=status.HTTP_400_BAD_REQUEST)
        response = super().post(request, *args, **kwargs)
        # Check if token is in cache
        if cache.get(token):
            return response
        else:
            if response.status_code == status.HTTP_200_OK:
                # Add token to cache with a short expiry time
                cache.set(token, 'valid', timeout=60 * 5)  # 5 minutes
            return response


class PasswordResetRequestAPIView(APIView):
    serializer_class = UserEmailResetSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Generate OTP
        otp_code = get_random_string(length=6, allowed_chars='0123456789')

        # Send OTP code via email
        subject = 'Password Reset OTP'
        message = f'Your OTP code for password reset is: {otp_code}'
        from_email = settings.EMAIL_HOST_USER
        to_email = [email]
        OTPCode.objects.update_or_create(user=user, defaults={"code": otp_code})
        try:
            send_mail(subject, message, from_email, to_email)  # TODO: convert to celery task
        except Exception as e:
            logging.error(str(e))
            pass
        # You may want to save the OTP code in the user's profile or create a separate model to store OTP codes

        return Response({
            "message": "An OTP code has been sent to your email address.",
            "otp": otp_code
        },
            status=status.HTTP_200_OK)


class ConfirmOTPAPIView(APIView):
    serializer_class = ConfirmOTPSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)
        if hasattr(user, "otp"):
            if user.otp.code == code:
                refresh = RefreshToken.for_user(user)
                access = refresh.access_token

                return Response({
                    "message": "OTP code is valid.",
                    "refresh": str(refresh),
                    "access": str(access)
                }, status=status.HTTP_200_OK)
            return Response({"code": ["OTP code is invalid"]}, status=status.HTTP_400_BAD_REQUEST)

        # You may want to save the OTP code in the user's profile or create a separate model to store OTP codes

        return Response({"message": ["An OTP code has been sent to your email address."]},
                        status=status.HTTP_200_OK)


class ChangePasswordAPIView(APIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        password = request.data.get('password')
        user = request.user
        user.password = make_password(password)
        user.save()

        # You may want to save the OTP code in the user's profile or create a separate model to store OTP codes

        return Response({"message": ["Password has changed"]}, status=status.HTTP_200_OK)
