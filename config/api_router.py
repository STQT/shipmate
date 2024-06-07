from django.conf import settings
from django.urls import path, include

from shipmate.company_management.views import MerchantViewSet, VoIPViewSet, TemplateViewSet
from shipmate.contract.views import GroundViewSet, HawaiiViewSet, InternationalViewSet
from rest_framework.routers import DefaultRouter, SimpleRouter

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

app_name = "api"

router.register(r'contracts/grounds', GroundViewSet)
router.register(r'contracts/hawaii', HawaiiViewSet)
router.register(r'contracts/internationals', InternationalViewSet)
router.register(r'merchant', MerchantViewSet)
router.register(r'voip', VoIPViewSet)
router.register(r'template', TemplateViewSet)

urlpatterns = router.urls

urlpatterns += [
    path('address/', include('shipmate.addresses.urls'), name="addresses"),
    path('quote/', include('shipmate.quotes.urls'), name="quotes"),
    path('leads/', include('shipmate.leads.urls'), name="leades"),
    path('orders/', include('shipmate.orders.urls'), name="orders"),
    path('cars/', include('shipmate.cars.urls'), name="cars"),
    path('customers/', include('shipmate.customers.urls'), name="customers"),
    path('providers/', include('shipmate.lead_managements.urls'), name="providers"),
    path('attachments/', include('shipmate.attachments.urls'), name="attachments"),
    path('users/', include('shipmate.users.urls'), name="users"),
    path('carriers/', include('shipmate.carriers.urls'), name="carriers"),
    path('company-management/', include('shipmate.company_management.urls'), name="company-management"),
    path('fields/', include('shipmate.mails.urls'), name="fields"),
]
