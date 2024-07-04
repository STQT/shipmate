from django.urls import path

from .utils import parsing_email, text
from .views import StaticDictView, GetCDPriceAPIView

urlpatterns = [
    path('list/', StaticDictView.as_view(), name='static-dict'),
    path('cd-price/<str:obj>/<uuid:guid>/', GetCDPriceAPIView.as_view(), name='cd-price-dict'),
]
# parsing_email(text, email="A01@email.com")
