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
    AttachmentDeleteAPIView,
)

urlpatterns = [
    path('', ListLeadsAPIView.as_view(), name='leads-list'),
    path('create/', CreateLeadsAPIView.as_view(), name='leads-create'),

    path('vehicle/add/', CreateVehicleLeadsAPIView.as_view(), name='leads-add-vehicle'),
    path('vehicle/<int:pk>/', RetrieveUpdateDestroyVehicleLeadsAPIView.as_view(),
         name='leads-add-vehicle'),

    path("attachments/<int:leadId>/", LeadsAttachmentListView.as_view(), name="leads-attachments"),
    path('attachments/delete/<int:id>/', AttachmentDeleteAPIView.as_view(), name='attachment-delete'),

    path('<str:guid>/update/', UpdateLeadsAPIView.as_view(), name='leads-update'),
    path('<str:guid>/detail/', DetailLeadsAPIView.as_view(), name='leads-detail'),
    path('<str:guid>/delete/', DeleteLeadsAPIView.as_view(), name='leads-delete'),
    path('<str:guid>/convert/', ConvertLeadToQuoteAPIView.as_view(), name='leads-to-quote'),

]
