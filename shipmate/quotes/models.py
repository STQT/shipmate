from django.db import models

from shipmate.contrib.models import QuoteAbstract


class Quote(QuoteAbstract):
    origin = models.ForeignKey("addresses.City", on_delete=models.SET_NULL, null=True, related_name='quotes_origin')
    destination = models.ForeignKey("addresses.City", on_delete=models.SET_NULL, null=True,
                                    related_name='quotes_destination')

    class Meta:
        verbose_name = "Quote"
        verbose_name_plural = "Quotes"
