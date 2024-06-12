from django.urls import path
from .views import (
    ListOrderAPIView,
    CreateOrderAPIView,
    UpdateOrderAPIView,
    DeleteOrderAPIView,
    DetailOrderAPIView,
    ArchiveListOrderAPIView,
    CreateVehicleOrderAPIView,
    RetrieveUpdateDestroyVehicleOrderAPIView, ProviderOrderListAPIView, OrderAttachmentDeleteAPIView,
    OrderAttachmentListView, DispatchingOrderCreateAPIView, ListOrderLogAPIView, DirectDispatchOrderCreateAPIView,
    ConvertQuoteToOrderAPIView, BackToQuoteOrderAPIView, PostToCDAPIView, CreateOrderContractAPIView
)

urlpatterns = [
    path('', ListOrderAPIView.as_view(), name='order-list'),
    path('providers/', ProviderOrderListAPIView.as_view(), name='order-provider-list'),
    path('archive/list/', ArchiveListOrderAPIView.as_view(), name='order-archive-list'),
    path('create/', CreateOrderAPIView.as_view(), name='order-create'),
    path('dispatch/<str:guid>/', DispatchingOrderCreateAPIView.as_view(), name='order-dispatch'),
    path('direct-dispatch/<str:guid>/', DirectDispatchOrderCreateAPIView.as_view(),
         name='order-direct-dispatch'),
    path('post-cd/<str:guid>/', PostToCDAPIView.as_view(), name='post-to-cd'),

    path('vehicle/add/', CreateVehicleOrderAPIView.as_view(), name='order-add-vehicle'),
    path('vehicle/<int:pk>/', RetrieveUpdateDestroyVehicleOrderAPIView.as_view(),
         name='order-add-vehicle'),
    path('contract/add/', CreateOrderContractAPIView.as_view(), name='order-add-contract'),

    path("attachments/<int:ordersId>/", OrderAttachmentListView.as_view(), name="order-attachments"),
    path('attachments/delete/<int:id>/', OrderAttachmentDeleteAPIView.as_view(), name='order-attachment-delete'),

    path('update/<str:guid>/', UpdateOrderAPIView.as_view(), name='order-update'),
    path('detail/<str:guid>/', DetailOrderAPIView.as_view(), name='order-detail'),
    path('delete/<str:guid>/', DeleteOrderAPIView.as_view(), name='order-delete'),
    path('logs/<int:order>/', ListOrderLogAPIView.as_view(), name='order-log-list'),
    path('convert/from-quote/<int:quote>/', ConvertQuoteToOrderAPIView.as_view(), name='quote-convert-order'),
    path('back-to-quote/<int:order>/', BackToQuoteOrderAPIView.as_view(), name='back-to-quote'),
]
