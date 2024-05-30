from django.utils import timezone


def log_update(sender, instance, created, log_klass, field_name, **kwargs):
    timestamp = timezone.now()
    updated_user_name = instance.updated_from.name if instance.updated_from else "Anonym"
    if not created:
        title = ""
        message = ""
        print(dir(instance))
        # Log all the updated fields
        for field in instance._meta.fields:
            field_name = field.name
            old_field_name = f"get_old_{field_name}"

            if hasattr(instance, old_field_name):
                old_value = getattr(instance, old_field_name)()
                new_value = getattr(instance, field_name)
                if old_value != new_value:
                    title += (f"- {field_name} field is edited on "
                              f"{timestamp.strftime('%B %d, %Y %I:%M %p')} by {updated_user_name}\n")
                    message += f"- {old_value} -> {new_value}\n"
        print(title)
        # Save log entry if any changes detected
        if title:
            data = {
                field_name: instance,
                "title": title,
                "message": message
            }
            log_klass.objects.create(**data)
    else:
        title = f"Lead provider is created on: {timestamp.strftime('%B %d, %Y %I:%M %p')} by {updated_user_name}\n"
        data = {
            field_name: instance,
            "title": title
        }
        log_klass.objects.create(**data)
