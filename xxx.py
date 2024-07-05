import uuid

from django.db import models

from shipmate.leads.models import Leads


def clone(record, guid=None):
    data = {field.name: getattr(record, field.name) for field in record._meta.fields if
            not isinstance(field, (models.AutoField, models.DateTimeField))}
    if guid:
        data['guid'] = str(uuid.uuid4())
    cloned_record = record.__class__.objects.create(**data)
    cloned_record.save()
    return cloned_record


def clone_record_with_related(record):
    cloned_record = clone(record, str(uuid.uuid4()))
    related_records = record.lead_attachments.all()
    for related_record in related_records:
        cloned_related_record = clone(related_record)
        cloned_related_record.lead = cloned_record
        cloned_related_record.save()
    related_records_vehicles = record.lead_vehicles.all()
    for related_record in related_records_vehicles:
        cloned_related_record = clone(related_record)
        cloned_related_record.lead = cloned_record
        cloned_related_record.save()
    return cloned_record


for lead in Leads.objects.all():
    clone_record_with_related(lead)
