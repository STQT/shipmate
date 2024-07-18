from django.urls import path

from .views import StaticDictView, GetCDPriceAPIView, GlobalSearchAPIView, GlobalSearchIDAPIView

urlpatterns = [
    path('list/', StaticDictView.as_view(), name='static-dict'),
    path('cd-price/<str:obj>/<uuid:guid>/', GetCDPriceAPIView.as_view(), name='cd-price-dict'),
    path('global-search/<str:type>/<str:q>/', GlobalSearchAPIView.as_view(), name='global-search'),
    path('global-search-id/<int:pk>/', GlobalSearchIDAPIView.as_view(), name='global-search'),



]
