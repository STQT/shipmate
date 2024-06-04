from django.urls import path
from .views import CompanyInfoDetail

urlpatterns = [
    path('info/<int:pk>/', CompanyInfoDetail.as_view(), name='company-info-detail'),
]
