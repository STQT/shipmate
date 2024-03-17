from django.db import models

from shipmate.contrib.models import LeadsAbstract


class Leads(LeadsAbstract):
    origin = models.ForeignKey("addresses.City", on_delete=models.SET_NULL, null=True, related_name='leads_origin')
    destination = models.ForeignKey("addresses.City", on_delete=models.SET_NULL, null=True,
                                    related_name='leads_destination')

    class Meta:
        verbose_name = "Lead"
        verbose_name_plural = "Leads"
