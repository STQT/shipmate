from django.db import models

from shipmate.contrib.models import LeadsAbstract, Attachments, VehicleAbstract


class Leads(LeadsAbstract):
    origin = models.ForeignKey("addresses.City", on_delete=models.SET_NULL, null=True, related_name='leads_origin')
    destination = models.ForeignKey("addresses.City", on_delete=models.SET_NULL, null=True,
                                    related_name='leads_destination')

    class Meta:
        verbose_name = "Lead"
        verbose_name_plural = "Leads"


class LeadsAttachment(Attachments):
    lead = models.ForeignKey(Leads, on_delete=models.CASCADE)

    class Meta:
        default_related_name = "lead_attachments"


class LeadVehicles(VehicleAbstract):
    lead = models.ForeignKey(Leads, on_delete=models.CASCADE)

    class Meta:
        default_related_name = "lead_vehicles"
