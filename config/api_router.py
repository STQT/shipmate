from django.conf import settings
from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter

from shipmate.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)

app_name = "api"
urlpatterns = router.urls

urlpatterns += [
    path('address/', include('shipmate.addresses.urls'), name="addresses"),
    path('quote/', include('shipmate.quotes.urls'), name="quotes"),
    path('leads/', include('shipmate.leads.urls'), name="leades"),
    path('cars/', include('shipmate.cars.urls'), name="cars"),
    path('customers/', include('shipmate.customers.urls'), name="customers"),
    path('providers/', include('shipmate.lead_managements.urls'), name="providers")
]
