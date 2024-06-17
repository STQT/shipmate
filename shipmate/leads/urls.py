from django.urls import path
from .views import (
    ListLeadsAPIView,
    CreateLeadsAPIView,
    UpdateLeadsAPIView,
    DeleteLeadsAPIView,
    DetailLeadsAPIView,
    ConvertLeadToQuoteAPIView,
    LeadsAttachmentListView,
    CreateVehicleLeadsAPIView,
    RetrieveUpdateDestroyVehicleLeadsAPIView,
    AttachmentDeleteAPIView, ProviderLeadListAPIView, ListLeadLogAPIView, ReAssignLeadView, ArchiveLeadView,
    ListTeamLeadAPIView,
)

urlpatterns = [
    path('', ListLeadsAPIView.as_view(), name='leads-list'),
    path('providers/', ProviderLeadListAPIView.as_view(), name='leads-provider-list'),
    path('teams/', ListTeamLeadAPIView.as_view(), name='leads-team-list'),
    path('create/', CreateLeadsAPIView.as_view(), name='leads-create'),

    path('vehicle/add/', CreateVehicleLeadsAPIView.as_view(), name='leads-add-vehicle'),
    path('vehicle/<int:pk>/', RetrieveUpdateDestroyVehicleLeadsAPIView.as_view(),
         name='leads-add-vehicle'),

    path("attachments/<int:leadId>/", LeadsAttachmentListView.as_view(), name="leads-attachments"),
    path('attachments/delete/<int:id>/', AttachmentDeleteAPIView.as_view(), name='attachment-delete'),

    path('reason/reassign/<uuid:guid>/', ReAssignLeadView.as_view(), name='reason-reassign'),
    path('reason/archive/<uuid:guid>/', ArchiveLeadView.as_view(), name='reason-archive'),

    path('update/<str:guid>/', UpdateLeadsAPIView.as_view(), name='leads-update'),
    path('detail/<str:guid>/', DetailLeadsAPIView.as_view(), name='leads-detail'),
    path('delete/<str:guid>/', DeleteLeadsAPIView.as_view(), name='leads-delete'),
    path('convert/<str:guid>/', ConvertLeadToQuoteAPIView.as_view(), name='leads-to-quote'),
    path('logs/<int:lead>/', ListLeadLogAPIView.as_view(), name='lead-log-list'),

]
