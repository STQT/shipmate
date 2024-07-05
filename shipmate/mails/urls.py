from django.urls import path

from .utils import parsing_email, text
from .views import StaticDictView, GetCDPriceAPIView, GlobalSearchAPIView

urlpatterns = [
    path('list/', StaticDictView.as_view(), name='static-dict'),
    path('cd-price/<str:obj>/<uuid:guid>/', GetCDPriceAPIView.as_view(), name='cd-price-dict'),
    path('global-search/<str:q>/', GlobalSearchAPIView.as_view(), name='global-search'),
]
# parsing_email(text, "admin@admin.admin")
