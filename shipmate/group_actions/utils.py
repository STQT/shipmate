from enum import Enum

from shipmate.leads.models import Leads, LeadsAttachment
from shipmate.quotes.models import Quote, QuoteAttachment
from shipmate.orders.models import Order, OrderAttachment


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
