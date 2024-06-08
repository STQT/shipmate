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
    AttachmentDeleteAPIView, ProviderLeadListAPIView, ListLeadLogAPIView,
)
from ..orders.views import DispatchOrderAPIView

urlpatterns = [
    path('', ListLeadsAPIView.as_view(), name='leads-list'),
    path('providers/', ProviderLeadListAPIView.as_view(), name='leads-provider-list'),
    path('create/', CreateLeadsAPIView.as_view(), name='leads-create'),

    path('vehicle/add/', CreateVehicleLeadsAPIView.as_view(), name='leads-add-vehicle'),
    path('vehicle/<int:pk>/', RetrieveUpdateDestroyVehicleLeadsAPIView.as_view(),
         name='leads-add-vehicle'),

    path("attachments/<int:leadId>/", LeadsAttachmentListView.as_view(), name="leads-attachments"),
    path('attachments/delete/<int:id>/', AttachmentDeleteAPIView.as_view(), name='attachment-delete'),

    path('update/<str:guid>/', UpdateLeadsAPIView.as_view(), name='leads-update'),
    path('detail/<str:guid>/', DetailLeadsAPIView.as_view(), name='leads-detail'),
    path('delete/<str:guid>/', DeleteLeadsAPIView.as_view(), name='leads-delete'),
    path('order/dispatch/<str:guid>/', DispatchOrderAPIView.as_view(), name='order-dispatch'),
    path('convert/<str:guid>/', ConvertLeadToQuoteAPIView.as_view(), name='leads-to-quote'),
    path('logs/<int:lead>/', ListLeadLogAPIView.as_view(), name='lead-log-list'),

]
