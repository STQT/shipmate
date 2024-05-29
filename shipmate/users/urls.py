from django.urls import path
from .views import (
    UserMeAPIView,
    MyTokenObtainPairView,
    MyTokenRefreshView,
    MyTokenVerifyView,

    FeatureCreateAPIView,
    FeatureDetailAPIView,
    FeatureListAPIView,
    FeatureUpdateAPIView,
    FeatureDestroyAPIView,

    TeamCreateAPIView,
    TeamDetailAPIView,
    TeamListAPIView,
    TeamUpdateAPIView,
    TeamDestroyAPIView,

    RoleCreateAPIView,
    RoleDetailAPIView,
    RoleListAPIView,
    RoleUpdateAPIView,
    RoleDestroyAPIView,

    PasswordResetRequestAPIView,
    ConfirmOTPAPIView,
    ChangePasswordAPIView,
    UserCreateViewSet,
    UserListViewSet,
    UserUpdateViewSet,
    UserDetailViewSet
)

urlpatterns = [
    path('create/', UserCreateViewSet.as_view(), name='create'),  # Create
    path('list/', UserListViewSet.as_view(), name='user-list'),
    path('detail/<int:pk>/', UserDetailViewSet.as_view(), name='user-detail'),
    path('update/<int:pk>/', UserUpdateViewSet.as_view(), name='user-update'),

    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login
    path('token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),  # Refresh token
    path('token/verify/', MyTokenVerifyView.as_view(), name='token_verify'),  # Verify token
    path('reset-password-request/', PasswordResetRequestAPIView.as_view(), name='reset-password'),
    path('confirm-otp/', ConfirmOTPAPIView.as_view(), name='confirm-otp'),  # Verify token
    path('change-password/', ChangePasswordAPIView.as_view(), name='change-password'),  # Verify token
    path('me/', UserMeAPIView.as_view(), name='user-me'),

    path('feature/', FeatureListAPIView.as_view(), name='feature-list'),
    path('feature/create/', FeatureCreateAPIView.as_view(), name='feature-create'),
    path('feature/update/<int:pk>/', FeatureUpdateAPIView.as_view(), name='feature-update'),
    path('feature/detail/<int:pk>/', FeatureDetailAPIView.as_view(), name='feature-detail'),
    path('feature/delete/<int:pk>/', FeatureDestroyAPIView.as_view(), name='feature-delete'),

    path('team/', TeamListAPIView.as_view(), name='team-list'),
    path('team/create/', TeamCreateAPIView.as_view(), name='team-create'),
    path('team/update/<int:pk>/', TeamUpdateAPIView.as_view(), name='team-update'),
    path('team/detail/<int:pk>/', TeamDetailAPIView.as_view(), name='team-detail'),
    path('team/delete/<int:pk>/', TeamDestroyAPIView.as_view(), name='team-delete'),

    path('role/', RoleListAPIView.as_view(), name='role-list'),
    path('role/create/', RoleCreateAPIView.as_view(), name='role-create'),
    path('role/update/<int:pk>/', RoleUpdateAPIView.as_view(), name='role-update'),
    path('role/detail/<int:pk>/', RoleDetailAPIView.as_view(), name='role-detail'),
    path('role/delete/<int:pk>/', RoleDestroyAPIView.as_view(), name='role-delete'),

]
