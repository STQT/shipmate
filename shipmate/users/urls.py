from django.urls import path
from .views import (
    UserMeAPIView,
    MyTokenObtainPairView,
    MyTokenRefreshView,
    MyTokenVerifyView,
    FeatureCreateAPIView, FeatureDetailAPIView, FeatureListAPIView, FeatureUpdateAPIView, FeatureDestroyAPIView,
    RoleCreateAPIView, RoleDetailAPIView, RoleListAPIView, RoleUpdateAPIView, RoleDestroyAPIView,
)

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login
    path('token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),  # Refresh token
    path('token/verify/', MyTokenVerifyView.as_view(), name='token_verify'),  # Verify token
    path('me/', UserMeAPIView.as_view(), name='user-me'),

    path('feature/', FeatureListAPIView.as_view(), name='feature-list'),
    path('feature/create/', FeatureCreateAPIView.as_view(), name='feature-create'),
    path('feature/<int:pk>/update/', FeatureUpdateAPIView.as_view(), name='feature-update'),
    path('feature/<int:pk>/detail/', FeatureDetailAPIView.as_view(), name='feature-detail'),
    path('feature/<int:pk>/delete/', FeatureDestroyAPIView.as_view(), name='feature-delete'),

    path('role/', RoleListAPIView.as_view(), name='role-list'),
    path('role/create/', RoleCreateAPIView.as_view(), name='role-create'),
    path('role/<int:pk>/update/', RoleUpdateAPIView.as_view(), name='role-update'),
    path('role/<int:pk>/detail/', RoleDetailAPIView.as_view(), name='role-detail'),
    path('role/<int:pk>/delete/', RoleDestroyAPIView.as_view(), name='role-delete'),

]
