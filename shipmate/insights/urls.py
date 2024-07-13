from django.urls import path
from .views import (
    GoalCreateAPIView,
    GoalDetailAPIView,
    GoalListAPIView,
    GoalUpdateAPIView,
    GoalDestroyAPIView,

)

urlpatterns = [
    path('goal/', GoalListAPIView.as_view(), name='goal-list'),
    path('goal/create/', GoalCreateAPIView.as_view(), name='goal-create'),
    path('goal/update/<int:pk>/', GoalUpdateAPIView.as_view(), name='goal-update'),
    path('goal/detail/<int:pk>/', GoalDetailAPIView.as_view(), name='goal-detail'),
    path('goal/delete/<int:pk>/', GoalDestroyAPIView.as_view(), name='goal-delete'),
]
