from django.urls import path
from .views import StaticDictView

urlpatterns = [
    path('list/', StaticDictView.as_view(), name='static-dict'),
]
