from django.urls import path
from .views import (
    AutomationCreateAPIView,
    AutomationDetailAPIView,
    AutomationListAPIView,
    AutomationUpdateAPIView,
    AutomationDestroyAPIView,

)

urlpatterns = [
    path('automation/', AutomationListAPIView.as_view(), name='automation-list'),
    path('automation/create/', AutomationCreateAPIView.as_view(), name='automation-create'),
    path('automation/update/<int:pk>/', AutomationUpdateAPIView.as_view(), name='automation-update'),
    path('automation/detail/<int:pk>/', AutomationDetailAPIView.as_view(), name='automation-detail'),
    path('automation/delete/<int:pk>/', AutomationDestroyAPIView.as_view(), name='automation-delete'),

]
