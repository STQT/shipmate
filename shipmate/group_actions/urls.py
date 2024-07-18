from django.urls import path
from .views import GroupReassignView

urlpatterns = [
    path('reassign/', GroupReassignView.as_view(), name='reassign'),
]
