from django.urls import path
from .views import UserMeAPIView, MyTokenObtainPairView, MyTokenRefreshView, MyTokenVerifyView

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login
    path('token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),  # Refresh token
    path('token/verify/', MyTokenVerifyView.as_view(), name='token_verify'),  # Verify token
    path('me/', UserMeAPIView.as_view(), name='user-me'),
]
