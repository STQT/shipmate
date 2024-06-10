from django.urls import path
from .views import (
    CompanyInfoDetail, LeadParsingGroupAllListView, LeadParsingValuePUTView, CreateLeadParsingValueView,
    LeadParsingGroupListView, LeadParsingItemListView, LeadParsingValueDeleteView
)

urlpatterns = [
    path('info/<int:pk>/', CompanyInfoDetail.as_view(), name='company-info-detail'),
    path('parsing-group-all/list/', LeadParsingGroupAllListView.as_view(), name='lead-parsing-all-group'),
    path('parsing-group/list/', LeadParsingGroupListView.as_view(), name='lead-parsing-group'),
    path('parsing-item/list/', LeadParsingItemListView.as_view(), name='lead-parsing-item'),
    path('parsing-value/create/', CreateLeadParsingValueView.as_view(), name='parsing-value-create'),
    path('parsing-value/delete/<int:pk>/', LeadParsingValueDeleteView.as_view(), name='parsing-value-delete'),
    path('parsing-value/update/<int:pk>/', LeadParsingValuePUTView.as_view(), name='parsing-value-edit'),
]
