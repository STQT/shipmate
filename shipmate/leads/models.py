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

    @property
    def origin_name(self):
        city_name = "NaN"  # noqa
        state_code = "NaN"
        city_zip = "NaN"

        if self.origin:
            if self.origin.state:
                city_name = self.origin.name
                state_code = self.origin.state.code
            city_zip = self.origin.zip

        return f"{city_name}, {state_code} {city_zip}"

    @property
    def destination_name(self):
        city_name = "NaN"  # noqa
        state_code = "NaN"
        city_zip = "NaN"

        if self.destination:
            if self.destination.state:
                city_name = self.destination.name
                state_code = self.destination.state.code
            city_zip = self.destination.zip

        return f"{city_name}, {state_code} {city_zip}"


class LeadsAttachment(Attachments):
    lead = models.ForeignKey(Leads, on_delete=models.CASCADE)
    

    class Meta:
        default_related_name = "lead_attachments"


class LeadAttachmentComment(models.Model):
    attachment = models.ForeignKey(LeadsAttachment, on_delete=models.CASCADE, related_name="lead_attachment_comments")
    text = models.TextField()

    def __str__(self):
        return f"{self.attachment} | {self.text}"


class LeadVehicles(VehicleAbstract):
    lead = models.ForeignKey(Leads, on_delete=models.CASCADE)

    class Meta:
        default_related_name = "lead_vehicles"


class LeadsLog(BaseLog):
    lead = models.ForeignKey("Leads", on_delete=models.CASCADE, related_name="logs")
