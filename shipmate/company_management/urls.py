from django.urls import path
from .views import CompanyInfoDetail, LeadParsingGroupListView, LeadParsingValuePUTView, CreateLeadParsingValueView

urlpatterns = [
    path('info/<int:pk>/', CompanyInfoDetail.as_view(), name='company-info-detail'),
    path('parsing-group/list/', LeadParsingGroupListView.as_view(), name='lead-parsing-group'),
    path('parsing-value/create/', CreateLeadParsingValueView.as_view(), name='parsing-value-create'),
    path('parsing-value/update/<int:pk>/', LeadParsingValuePUTView.as_view(), name='parsing-value-edit'),
]
