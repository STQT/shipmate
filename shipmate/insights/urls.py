from django.urls import path
from .views import (
    GoalCreateAPIView,
    GoalDetailAPIView,
    GoalListAPIView,
    GoalUpdateAPIView,
    GoalDestroyAPIView, LeadsInsightUsersAPIView, LeadsInsightDaysAPIView, LeadsInsightAPIView,

)

urlpatterns = [
    path('goal/', GoalListAPIView.as_view(), name='goal-list'),
    path('goal/create/', GoalCreateAPIView.as_view(), name='goal-create'),
    path('goal/update/<int:pk>/', GoalUpdateAPIView.as_view(), name='goal-update'),
    path('goal/detail/<int:pk>/', GoalDetailAPIView.as_view(), name='goal-detail'),
    path('goal/delete/<int:pk>/', GoalDestroyAPIView.as_view(), name='goal-delete'),
    path('lead-insight/users/', LeadsInsightUsersAPIView.as_view(), name='lead-insight-users'),
    path('lead-insight/days/', LeadsInsightDaysAPIView.as_view(), name='lead-insight-days'),
    path('lead-insight/', LeadsInsightAPIView.as_view(), name='lead-insight-list'),

]
