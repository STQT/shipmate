from django.urls import path
from .views import GroupReassignView, GroupEmailSendView, GroupSMSSendView, GroupArchiveView

urlpatterns = [
    path('reassign/', GroupReassignView.as_view(), name='reassign'),
    path('archive/', GroupArchiveView.as_view(), name='archive'),
    path('email/', GroupEmailSendView.as_view(), name='email'),
    path('sms/', GroupSMSSendView.as_view(), name='sms'),
]
