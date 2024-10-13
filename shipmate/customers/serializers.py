from datetime import date

from rest_framework import serializers
from django.db import models

from .models import Customer, ExternalContacts
from ..contrib.models import OrderStatusChoices
from ..leads.models import Leads
from ..orders.models import Order
from ..payments.models import OrderPaymentCreditCard, OrderPayment


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"

    def validate_phone(self, value):
        cleaned_value = value.replace("-", "").replace("(", "").replace(")", "").replace(" ", "")
        return cleaned_value

    def create(self, validated_data):
        validated_data['phone'] = self.validate_phone(validated_data.get('phone', ''))
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['phone'] = self.validate_phone(validated_data.get('phone', instance.phone))
        return super().update(instance, validated_data)


class RetrieveCustomerSerializer(serializers.ModelSerializer):
    phone = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = "__all__"

    @classmethod
    def get_phone(cls, obj) -> str:
        phone = obj.phone if obj.phone else "NaN"
        if phone and len(phone) == 10:  # Assuming phone is a 10-digit number
            return f"({phone[:3]}) {phone[3:6]}-{phone[6:]}"
        return phone


class ExternalContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalContacts
        fields = "__all__"


class SmallExternalContactsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    phone = serializers.CharField()


class DetailCustomerSerializer(serializers.ModelSerializer):
    extra = SmallExternalContactsSerializer(many=True)
    completed = serializers.SerializerMethodField()
    ongoing = serializers.SerializerMethodField()
    uncompleted = serializers.SerializerMethodField()
    source = serializers.SerializerMethodField()
    stage = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    # attached_payment_methods = serializers.SerializerMethodField()
    # payments_made = serializers.SerializerMethodField()
    # charged = serializers.SerializerMethodField()
    # refunded = serializers.SerializerMethodField()
    # sent_to_carrier = serializers.SerializerMethodField()
    # chargeback = serializers.SerializerMethodField()


    class Meta:
        model = Customer
        fields = "__all__"

    @classmethod
    def get_completed(self, obj):
        # Get all related orders and sum the reservation fee (payment_reservation)
        orders = Order.objects.filter(customer_id=obj.id)
        total_reservation_fee = orders.aggregate(total=models.Sum('payment_paid_reservation'))['total']
        return total_reservation_fee or 0  # Return 0 if there are no orders


    @classmethod
    def get_ongoing(self, obj):
        # Define the statuses for ongoing orders
        ongoing_statuses = [
            OrderStatusChoices.ORDERS,
            OrderStatusChoices.BOOKED,
            OrderStatusChoices.POSTED,
            OrderStatusChoices.NOTSIGNED
        ]
        # Filter orders by user and ongoing statuses
        orders = Order.objects.filter(customer_id=obj.id, status__in=ongoing_statuses)
        total_ongoing_reservation = orders.aggregate(total=models.Sum('payment_reservation'))['total']
        return total_ongoing_reservation or 0  # Return 0 if there are no ongoing orders

    # @classmethod
    # def get_ongoing(self, obj):
    #     # Define the statuses for ongoing orders
    #     ongoing_statuses = [
    #         OrderStatusChoices.ORDERS,
    #         OrderStatusChoices.BOOKED,
    #         OrderStatusChoices.POSTED,
    #         OrderStatusChoices.NOTSIGNED
    #     ]
    #
    #     # Filter orders by customer and ongoing statuses
    #     orders = Order.objects.filter(customer_id=obj.id, status__in=ongoing_statuses)
    #     order_list = []
    #     total_amount_sum = 0
    #
    #     # Process each ongoing order
    #     for order in orders:
    #         # Calculate the total amount
    #         total_amount = order.payment_total_tariff
    #         total_amount_sum += total_amount
    #
    #         # Get a human-readable ship date
    #         if order.date_est_ship:
    #             delta = (order.date_est_ship - date.today()).days
    #             if delta == 0:
    #                 ship_date = "today"
    #             elif delta == 1:
    #                 ship_date = "tomorrow"
    #             elif delta == -1:
    #                 ship_date = "yesterday"
    #             elif delta > 1:
    #                 ship_date = f"in {delta} days"
    #             else:
    #                 ship_date = f"{abs(delta)} days ago"
    #         else:
    #             ship_date = "N/A"
    #
    #         # Append order data to the list
    #         order_list.append({
    #             'id': order.id,
    #             'total_amount': total_amount,
    #             'status': order.status,
    #             'ship_date': ship_date
    #         })
    #
    #     # Add total amount sum to the list
    #     order_list.append({'total_amount_sum': total_amount_sum})
    #
    #     return order_list if order_list else 'No ongoing orders'

    @classmethod
    def get_uncompleted(self, obj):
        # Filter orders by user and Archived status
        orders = Order.objects.filter(customer_id=obj.id, status=OrderStatusChoices.ARCHIVED)
        total_uncompleted_reservation = orders.aggregate(total=models.Sum('payment_reservation'))['total']
        return total_uncompleted_reservation or 0  # Return 0 if there are no archived (uncompleted) orders

    @classmethod
    def get_source(self, obj):
        first_lead = Leads.objects.filter(customer_id=obj.id).first()
        if first_lead:
            return first_lead.source.name
        else:
            return 'NaN'

    @classmethod
    def get_address(self, obj):
        # Get the latest order of the customer that has related credit card data
        latest_order = Order.objects.filter(customer_id=obj.id, credit_cards__isnull=False).order_by(
            '-created_at').first()

        if latest_order:
            # Get the latest credit card information related to this order
            latest_credit_card = latest_order.credit_cards.last()  # Get the most recent credit card
            if latest_credit_card:
                # Build the full address from the credit card's billing details
                full_address = {
                    'billing_address': latest_credit_card.billing_address,
                    'billing_city': latest_credit_card.billing_city,
                    'billing_state': latest_credit_card.billing_state,
                    'billing_zip': latest_credit_card.billing_zip
                }
                return full_address
        return 'NaN'

    # @classmethod
    # def get_attached_payment_methods(self, obj):
    #     # Get all orders related to the customer
    #     orders = Order.objects.filter(customer_id=obj.id)
    #
    #     # Retrieve all the credit cards related to the customer's orders
    #     credit_cards = OrderPaymentCreditCard.objects.filter(order__in=orders)
    #
    #     # Format the credit card details
    #     payment_methods = []
    #     for card in credit_cards:
    #         payment_methods.append({
    #             'card_number': card.card_number,
    #             'first_name': card.first_name,
    #             'last_name': card.last_name,
    #             'expiration_date': card.expiration_date,
    #             'billing_address': card.billing_address,
    #             'billing_city': card.billing_city,
    #             'billing_state': card.billing_state,
    #             'billing_zip': card.billing_zip
    #         })
    #
    #     return payment_methods if payment_methods else 'No attached payment methods'

    # @classmethod
    # def get_payments_made(self, obj):
    #     # Get all orders related to the customer
    #     orders = Order.objects.filter(customer_id=obj.id)
    #
    #     # Filter payments related to these orders and that have the status 'charged'
    #     payments = OrderPayment.objects.filter(order__in=orders, status=OrderPayment.StatusChoices.CHARGE)
    #
    #     payment_list = []
    #     charged_sum, refunded_sum, sent_sum, chargeback_sum = 0, 0, 0, 0
    #
    #     for payment in payments:
    #         # Determine the amount format (+ or -) based on payment direction
    #         if payment.direction == OrderPayment.DirectionChoices.customer_to_broker:
    #             amount = f"+{payment.amount}"
    #             charged_sum += payment.amount  # Track charged amounts
    #         else:
    #             amount = f"-{payment.amount}"
    #             if payment.charge_type == OrderPayment.ChargeTypeChoices.refund:
    #                 refunded_sum += payment.amount
    #             elif payment.charge_type == OrderPayment.ChargeTypeChoices.sent:
    #                 sent_sum += payment.amount
    #             elif payment.charge_type == OrderPayment.ChargeTypeChoices.chargeback:
    #                 chargeback_sum += payment.amount
    #
    #         # Append payment details to the list
    #         payment_list.append({
    #             'id': payment.id,
    #             'amount': amount,
    #             'method_name': payment.payment_type,  # Payment method type (credit card, Zelle, etc.)
    #             'date': payment.created_at  # Payment creation date
    #         })
    #
    #     # Add total sum summaries at the end of the payment list
    #     payment_list.append({
    #         'Charged': charged_sum,
    #         'Refunded': refunded_sum,
    #         'Sent to carrier': sent_sum,
    #         'Chargeback': chargeback_sum
    #     })
    #
    #     return payment_list if payment_list else 'No payments made'

    # @classmethod
    # def get_charged(self, obj):
    #     orders = Order.objects.filter(customer_id=obj.id)
    #     charged_sum = \
    #     OrderPayment.objects.filter(order__in=orders, charge_type=OrderPayment.ChargeTypeChoices.charge).aggregate(
    #         total=models.Sum('amount'))['total']
    #     return charged_sum or 0
    #
    # @classmethod
    # def get_refunded(self, obj):
    #     orders = Order.objects.filter(customer_id=obj.id)
    #     refunded_sum = \
    #     OrderPayment.objects.filter(order__in=orders, charge_type=OrderPayment.ChargeTypeChoices.refund).aggregate(
    #         total=models.Sum('amount'))['total']
    #     return refunded_sum or 0
    #
    # @classmethod
    # def get_sent_to_carrier(self, obj):
    #     orders = Order.objects.filter(customer_id=obj.id)
    #     sent_sum = \
    #     OrderPayment.objects.filter(order__in=orders, charge_type=OrderPayment.ChargeTypeChoices.sent).aggregate(
    #         total=models.Sum('amount'))['total']
    #     return sent_sum or 0
    #
    # @classmethod
    # def get_chargeback(self, obj):
    #     orders = Order.objects.filter(customer_id=obj.id)
    #     chargeback_sum = \
    #     OrderPayment.objects.filter(order__in=orders, charge_type=OrderPayment.ChargeTypeChoices.chargeback).aggregate(
    #         total=models.Sum('amount'))['total']
    #     return chargeback_sum or 0

    @classmethod
    def get_stage(self, obj):
        last_order = Order.objects.filter(customer_id=obj.id).order_by('-id').first()
        if last_order:
            return last_order.status
        else:
            return 'NaN'

