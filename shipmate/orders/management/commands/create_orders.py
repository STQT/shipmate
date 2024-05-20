import random

from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from shipmate.orders.models import Order
from shipmate.contrib.models import OrderStatusChoices
from shipmate.addresses.models import City  # Adjust import as needed
from shipmate.customers.models import Customer  # Adjust import as needed
from shipmate.lead_managements.models import Provider  # Adjust import as needed

User = get_user_model()


class Command(BaseCommand):
    help = 'Create 5 orders for each status'

    def handle(self, *args, **kwargs):
        user = User.objects.first()  # Assuming you have at least one user
        if not user:
            self.stdout.write(self.style.ERROR('No users found in the database.'))
            return

        for status in OrderStatusChoices.choices:
            status_value = status[0]
            for i in range(5):
                order = Order.objects.create(
                    source=Provider.objects.order_by("?").first(),
                    customer=Customer.objects.order_by("?").first(),
                    buyer_number=f'{random.randint(100000, 999999)}',
                    user=user,
                    extra_user=None,  # Assuming no extra user
                    origin=City.objects.order_by('?').first(),
                    origin_business_name=f'Business_{random.randint(1000, 9999)}',
                    origin_business_phone=f'11-{random.randint(1000, 9999)}',
                    origin_contact_person=f'Person_{random.randint(1000, 9999)}',
                    origin_phone=f'11-{random.randint(1000, 9999)}',
                    origin_second_phone=f'11-{random.randint(1000, 9999)}',
                    origin_buyer_number=f'Buyer_{random.randint(1000, 9999)}',
                    destination=City.objects.order_by('?').first(),
                    destination_business_name=f'Business_{random.randint(1000, 9999)}',
                    destination_business_phone=f'555-{random.randint(1000, 9999)}',
                    destination_contact_person=f'Person_{random.randint(1000, 9999)}',
                    destination_phone=f'11-{random.randint(100000, 999999)}',
                    destination_second_phone=f'11-{random.randint(100000, 999999)}',
                    payment_total_tariff=random.randint(1000, 5000),
                    payment_reservation=random.randint(100, 500),
                    payment_paid_reservation=random.randint(100, 500),
                    payment_carrier_pay=random.randint(100, 500),
                    payment_cod_to_carrier=random.randint(100, 500),
                    payment_paid_to_carrier=random.randint(100, 500),
                    date_est_ship=timezone.now().date(),
                    date_est_pu=timezone.now().date(),
                    date_est_del=timezone.now().date(),
                    date_dispatched=timezone.now().date(),
                    date_picked_up=timezone.now().date(),
                    date_delivered=timezone.now().date(),
                    cd_note=f'CD Note {random.randint(1000, 9999)}',
                    cm_note=f'CM Note {random.randint(1000, 9999)}',
                    status=status_value,
                )
                self.stdout.write(self.style.SUCCESS(f'Created order {order.id} with status {status_value}'))

        self.stdout.write(self.style.SUCCESS('Finished creating orders'))
