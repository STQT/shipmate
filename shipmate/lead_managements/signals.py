from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Provider, ProviderLog


@receiver(post_save, sender=Provider)
def log_provider_update(sender, instance, created, **kwargs):
    timestamp = timezone.now()
    updated_user_name = instance.updated_from.user.name if instance.updated_from else "Anonym"
    if not created:
        title = ""
        message = ""

        # Log all the updated fields
        for field in instance._meta.fields:
            field_name = field.name
            old_value = getattr(instance, f"get_old_{field_name}")()
            new_value = getattr(instance, field_name)
            if old_value != new_value:
                title += (f"- {field_name} field is edited on "
                          f"{timestamp.strftime('%B %d, %Y %I:%M %p')} by {updated_user_name}\n")
                message += f"- {old_value} -> {new_value}\n"

        # Save log entry if any changes detected
        if title:
            ProviderLog.objects.create(provider=instance, title=title, message=message)
    else:
        title = f"Lead provider is created on: {timestamp.strftime('%B %d, %Y %I:%M %p')} by {updated_user_name}\n"
        ProviderLog.objects.create(provider=instance, title=title)
