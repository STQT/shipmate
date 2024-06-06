from django.contrib.auth import get_user_model
from django.db import models
from django.core.exceptions import ValidationError

from shipmate.contrib.models import LeadsAbstract, Attachments, VehicleAbstract
from shipmate.utils.models import BaseLog

User = get_user_model()


class Leads(LeadsAbstract):
    origin = models.ForeignKey("addresses.City", on_delete=models.SET_NULL, null=True, related_name='leads_origin')
    destination = models.ForeignKey("addresses.City", on_delete=models.SET_NULL, null=True,
                                    related_name='leads_destination')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leads_user')
    extra_user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,
                                   related_name='leads_extra_user')
    updated_from = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="+",
                                     null=True, blank=True)

    def clean(self):
        super().clean()

        if self.user_id == self.extra_user_id:
            raise ValidationError("User and Extra User cannot have equivalent values.")

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


class LeadsLog(BaseLog):
    lead = models.ForeignKey("Leads", on_delete=models.CASCADE, related_name="logs")
