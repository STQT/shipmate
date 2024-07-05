from django.urls import path

from .views import (
    ListQuoteAPIView,
    CreateQuoteAPIView,
    UpdateQuoteAPIView,
    DeleteQuoteAPIView,
    DetailQuoteAPIView,
    ArchiveListQuoteAPIView,
    CreateVehicleQuoteAPIView,
    RetrieveUpdateDestroyVehicleQuoteAPIView, ProviderQuoteListAPIView, QuoteAttachmentDeleteAPIView,
    QuoteAttachmentListView, ListQuoteLogAPIView, ArchiveQuoteView, ReAssignQuoteView, ListTeamQuoteAPIView
)

urlpatterns = [
    path('', ListQuoteAPIView.as_view(), name='quote-list'),
    path('providers/', ProviderQuoteListAPIView.as_view(), name='quote-provider-list'),
    path('teams/', ListTeamQuoteAPIView.as_view(), name='quote-team-list'),
    path('archive/list/', ArchiveListQuoteAPIView.as_view(), name='quote-archive-list'),
    path('create/', CreateQuoteAPIView.as_view(), name='quote-create'),

    path('vehicle/add/', CreateVehicleQuoteAPIView.as_view(), name='quote-add-vehicle'),
    path('vehicle/<int:pk>/', RetrieveUpdateDestroyVehicleQuoteAPIView.as_view(),
         name='quote-add-vehicle'),

    path('reason/reassign/<uuid:guid>/', ReAssignQuoteView.as_view(), name='reason-reassign'),
    path('reason/archive/<uuid:guid>/', ArchiveQuoteView.as_view(), name='reason-archive'),

    path("attachments/<int:quoteId>/", QuoteAttachmentListView.as_view(), name="quote-attachments"),
    path('attachments/delete/<int:id>/', QuoteAttachmentDeleteAPIView.as_view(), name='quote-attachment-delete'),

    path('update/<str:guid>/', UpdateQuoteAPIView.as_view(), name='quote-update'),
    path('detail/<str:guid>/', DetailQuoteAPIView.as_view(), name='quote-detail'),
    path('delete/<str:guid>/', DeleteQuoteAPIView.as_view(), name='quote-delete'),
    path('logs/<int:quote>/', ListQuoteLogAPIView.as_view(), name='quote-log-list'),
]
