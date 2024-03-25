from django.db import models

from shipmate.contrib.models import QuoteAbstract, Attachments


class Quote(QuoteAbstract):
    origin = models.ForeignKey("addresses.City", on_delete=models.SET_NULL, null=True, related_name='quotes_origin')
    destination = models.ForeignKey("addresses.City", on_delete=models.SET_NULL, null=True,
                                    related_name='quotes_destination')

    class Meta:
        verbose_name = "Quote"
        verbose_name_plural = "Quotes"


class QuoteAttachment(Attachments):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE)

    class Meta:
        default_related_name = "quotes"
