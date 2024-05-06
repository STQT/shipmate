from django.urls import path
from .views import (
    UserMeAPIView,
    MyTokenObtainPairView,
    MyTokenRefreshView,
    MyTokenVerifyView,
    FeatureCreateAPIView, FeatureDetailAPIView, FeatureListAPIView, FeatureUpdateAPIView, FeatureDestroyAPIView,
    RoleCreateAPIView, RoleDetailAPIView, RoleListAPIView, RoleUpdateAPIView, RoleDestroyAPIView,
    PasswordResetRequestAPIView, ConfirmOTPAPIView, ChangePasswordAPIView, UserCreateViewSet,
)

urlpatterns = [
    path('create/', UserCreateViewSet.as_view(), name='create'),  # Create
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login
    path('token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),  # Refresh token
    path('token/verify/', MyTokenVerifyView.as_view(), name='token_verify'),  # Verify token
    path('reset-password-request/', PasswordResetRequestAPIView.as_view(), name='reset-password'),  # Reset password
    path('confirm-otp/', ConfirmOTPAPIView.as_view(), name='confirm-otp'),  # Verify token
    path('change-password/', ChangePasswordAPIView.as_view(), name='change-password'),  # Verify token
    path('me/', UserMeAPIView.as_view(), name='user-me'),

    path('feature/', FeatureListAPIView.as_view(), name='feature-list'),
    path('feature/create/', FeatureCreateAPIView.as_view(), name='feature-create'),
    path('feature/update/<int:pk>/', FeatureUpdateAPIView.as_view(), name='feature-update'),
    path('feature/detail/<int:pk>/', FeatureDetailAPIView.as_view(), name='feature-detail'),
    path('feature/delete/<int:pk>/', FeatureDestroyAPIView.as_view(), name='feature-delete'),

    path('role/', RoleListAPIView.as_view(), name='role-list'),
    path('role/create/', RoleCreateAPIView.as_view(), name='role-create'),
    path('role/update/<int:pk>/', RoleUpdateAPIView.as_view(), name='role-update'),
    path('role/detail/<int:pk>/', RoleDetailAPIView.as_view(), name='role-detail'),
    path('role/delete/<int:pk>/', RoleDestroyAPIView.as_view(), name='role-delete'),

]
