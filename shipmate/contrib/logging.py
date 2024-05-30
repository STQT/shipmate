from django.utils import timezone


def store_old_values(sender, instance, **kwargs):
    if instance.pk:  # Check if the instance already exists in the database
        old_instance = sender.objects.get(pk=instance.pk)

        instance._old_values = {field.name: getattr(old_instance, field.name) for field in instance._meta.fields}
        print(instance._old_values)
    else:
        instance._old_values = {}


def log_update(sender, instance, created, log_klass, klas_field_name, **kwargs):
    timestamp = timezone.now()
    updated_user_name = (instance.updated_from.first_name + " " + instance.updated_from.last_name
                         if instance.updated_from else "Anonym")
    if not created:

        old_values = getattr(instance, '_old_values', {})
        # Log all the updated fields
        for field in instance._meta.fields:
            title = ""
            message = ""
            field_name = field.name
            old_value = old_values.get(field_name)
            new_value = getattr(instance, field_name)
            if old_value != new_value:
                title += (f"{field_name} field was edited on "
                          f"{timestamp.strftime('%B %d, %Y %I:%M %p')} by {updated_user_name}\n")
                message += f"{old_value}     →    {new_value}\n"

            if title:
                data = {
                    klas_field_name: instance,
                    'title': title,
                    'message': message
                }
                log_klass.objects.create(**data)
    else:
        title = f"Created on: {timestamp.strftime('%B %d, %Y %I:%M %p')} by {updated_user_name}\n"
        data = {
            klas_field_name: instance,
            "title": title
        }
        log_klass.objects.create(**data)
