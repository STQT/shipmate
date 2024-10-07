from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db import models

from shipmate.contrib.models import QuoteAbstract, Attachments, VehicleAbstract, QuoteStatusChoices
from shipmate.more_settings.models import Automation
from shipmate.utils.models import BaseLog
from shipmate.more_settings.tasks import send_automation_message


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

    def save(self, *args, **kwargs):
        is_new = self.pk is None  # Check if this is a new instance

        status_mapper = {
            QuoteStatusChoices.QUOTES: 'quoted',
            QuoteStatusChoices.FOLLOWUP: 'follow_up',
            QuoteStatusChoices.WARM: 'warm',
            QuoteStatusChoices.ONGOING: 'ongoing',
            QuoteStatusChoices.UPCOMING: 'upcoming',
            QuoteStatusChoices.ONHOLD: 'on_hold',
            QuoteStatusChoices.NOTNOW: 'not_now',
            QuoteStatusChoices.ARCHIVED: 'archived'
        }

        if not self.pk:
            self.created_at = timezone.now()
            self.updated_at = self.created_at

        else:
            old_instance = self.__class__.objects.get(pk=self.pk)
            if self.extra_user != old_instance.extra_user:
                self.updated_at = timezone.now()
                quote_dates, created = QuoteDates.objects.get_or_create(quote=self)
                quote_dates.re_assigned = self.updated_at
                quote_dates.save()
            if self.status != old_instance.status:
                self.updated_at = timezone.now()
                quote_dates, created = QuoteDates.objects.get_or_create(quote=self)
                status_date_field = status_mapper.get(self.status)
                if status_date_field:
                    setattr(quote_dates, status_date_field, timezone.now())
                    quote_dates.last_time_edited = self.updated_at
                    quote_dates.save()
        super().save(*args, **kwargs)
        if is_new:
            # Retrieve active automations for the given step
            active_automations = Automation.objects.filter(
                steps=Automation.StepsChoices.AFTER_QUOTED,  # Adjust step according to the flow
                status=Automation.StatusChoices.ACTIVE,
                included_users=self.user
            )
            for automation in active_automations:
                # Schedule the task after the specified delay
                try:
                    send_automation_message.apply_async(
                        args=[self.customer.email, self.user.phone, self.customer.phone, automation.id],  # Pass lead_id and automation_id
                        countdown=automation.delays_minutes * 60  # Delay in seconds
                    )
                except Exception as e:
                    print(e)
                    continue

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


class QuoteAttachment(Attachments):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE)
    time_took = models.CharField(null=True, blank=True, max_length=255)

    class Meta:
        default_related_name = "quotes"


class QuoteAttachmentComment(models.Model):
    attachment = models.ForeignKey(QuoteAttachment,
                                   on_delete=models.CASCADE, related_name="quote_attachment_comments")
    text = models.TextField()

    def __str__(self):
        return f"{self.attachment} | {self.text}"


class QuoteVehicles(VehicleAbstract):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE)

    class Meta:
        default_related_name = "quote_vehicles"


class QuoteLog(BaseLog):
    quote = models.ForeignKey("Quote", on_delete=models.CASCADE, related_name="logs")


class QuoteDates(models.Model):
    quote = models.OneToOneField('Quote', on_delete=models.CASCADE, related_name='quote_dates')
    last_time_edited = models.DateTimeField(blank=True, null=True)
    re_assigned = models.DateTimeField(blank=True, null=True)
    converted = models.DateTimeField(blank=True, null=True)
    quoted = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    received = models.DateTimeField(blank=True, null=True)
    follow_up = models.DateTimeField(blank=True, null=True)
    warm = models.DateTimeField(blank=True, null=True)
    ongoing = models.DateTimeField(blank=True, null=True)
    upcoming = models.DateTimeField(blank=True, null=True)
    on_hold = models.DateTimeField(blank=True, null=True)
    not_now = models.DateTimeField(blank=True, null=True)
    archived = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"QuoteDates for {self.quote}"


