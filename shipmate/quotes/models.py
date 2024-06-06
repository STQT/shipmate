from django.contrib.auth import get_user_model
from django.db import models

from shipmate.contrib.models import QuoteAbstract, Attachments, VehicleAbstract
from shipmate.utils.models import BaseLog

User = get_user_model()


class Quote(QuoteAbstract):
    origin = models.ForeignKey("addresses.City", on_delete=models.SET_NULL, null=True, related_name='quotes_origin')
    destination = models.ForeignKey("addresses.City", on_delete=models.SET_NULL, null=True,
                                    related_name='quotes_destination')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quote_user')
    extra_user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,
                                   related_name='quote_extra_user')
    updated_from = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="+",
                                     null=True, blank=True)

    class Meta:
        verbose_name = "Quote"
        verbose_name_plural = "Quotes"


class QuoteAttachment(Attachments):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE)

    class Meta:
        default_related_name = "quotes"


class QuoteVehicles(VehicleAbstract):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE)

    class Meta:
        default_related_name = "quote_vehicles"


class QuoteLog(BaseLog):
    quote = models.ForeignKey("Quote", on_delete=models.CASCADE, related_name="logs")
