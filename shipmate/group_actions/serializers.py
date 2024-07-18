from enum import Enum

from django.db import transaction
from rest_framework import serializers
from django.contrib.auth import get_user_model

from shipmate.contrib.models import Attachments
from shipmate.leads.models import Leads, LeadsAttachment
from shipmate.quotes.models import Quote, QuoteAttachment
from shipmate.orders.models import Order, OrderAttachment

User = get_user_model()


class AttachmentType(Enum):
    QUOTE = "quote"
    LEAD = "leads"
    ORDER = "order"


ATTACHMENT_CLASS_MAP = {
    AttachmentType.QUOTE.value: Quote,
    AttachmentType.LEAD.value: Leads,
    AttachmentType.ORDER.value: Order
}

ATTACHMENT_FK_FIELD_MAP = {
    AttachmentType.QUOTE.value: 'quote',
    AttachmentType.LEAD.value: 'lead',
    AttachmentType.ORDER.value: 'order'
}
ATTACHMENT_ATTACHMENT_MAP = {
    AttachmentType.QUOTE.value: QuoteAttachment,
    AttachmentType.LEAD.value: LeadsAttachment,
    AttachmentType.ORDER.value: OrderAttachment
}


class GroupReassignSerializer(serializers.Serializer):
    endpoint_type = serializers.ChoiceField(choices=[(tag.value, tag.name.title()) for tag in AttachmentType],
                                            write_only=True, required=False, allow_null=True)
    ids = serializers.ListField(child=serializers.IntegerField())
    user = serializers.IntegerField()
    reason = serializers.CharField()

    def validate_user(self, value):
        try:
            User.objects.get(pk=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")
        return value

    def create(self, validated_data):
        ids = validated_data['ids']
        endpoint_type = validated_data['endpoint_type']
        user_id = validated_data['user']
        reason = validated_data['reason']

        user = User.objects.get(pk=user_id)
        model_class = ATTACHMENT_CLASS_MAP[endpoint_type]
        fk_field = ATTACHMENT_FK_FIELD_MAP[endpoint_type]
        attachment_class = ATTACHMENT_ATTACHMENT_MAP[endpoint_type]

        objs = model_class.objects.filter(id__in=ids)
        if not objs.exists():
            raise serializers.ValidationError({fk_field: [f"{fk_field.capitalize()} not found"]})

        request_user = self.context['request'].user
        objs.update(user=user)
        attachment_objects = []
        for obj in objs:
            data = {
                fk_field: obj,
                "title": f'Reassigned to {user.first_name} {user.last_name}',
                "user": request_user,
                "second_title": f'Reason: {reason}',
                "type": Attachments.TypesChoices.ACTIVITY,
                "link": 0
            }
            attachment_objects.append(attachment_class(**data))
        attachment_class.objects.bulk_create(attachment_objects)
        return validated_data
