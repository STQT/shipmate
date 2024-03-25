from django.db import models

from shipmate.contrib.models import Attachments, OrderAbstract


class Order(OrderAbstract):
    origin = models.ForeignKey("addresses.City", on_delete=models.SET_NULL, null=True, related_name='orders_origin')
    destination = models.ForeignKey("addresses.City", on_delete=models.SET_NULL, null=True,
                                    related_name='orders_destination')

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"


class OrderAttachment(Attachments):
    lead = models.ForeignKey(Order, on_delete=models.CASCADE)

    class Meta:
        default_related_name = "orders"
