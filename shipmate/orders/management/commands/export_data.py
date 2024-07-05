from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Export leads data to a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file')

    def handle(self, *args, **kwargs):
        _csv_file = kwargs['csv_file']
        # with open(csv_file, 'w', newline='') as csvfile:
        #     writer = csv.writer(csvfile)
        #     writer.writerow([
        #         'id', 'date_entered', 'phone', 'email', 'first_name', 'last_name', 'vehicles',
        #         'pickup_zip', 'pickup_city', 'pickup_state_code', 'dropoff_zip', 'dropoff_city',
        #         'dropoff_state_code', 'price_total_total', 'estimated_ship_date', 'lead_status',
        #         'ship_via_id', 'vehicle_runs', 'provider_name', 'user_name'
        #     ])
        #
        #     for quote in Quote.objects.filter(
        #         created_at__gte=datetime.datetime()):
        #         writer.writerow([
        #             quote.id,
        #             quote.created_at,
        #             quote.customer.phone,
        #             quote.customer.email,
        #             quote.customer.name,
        #             quote.customer.last_name,
        #             quote.vehicles,
        #             quote.origin.zip_code,
        #             quote.origin.name,
        #             quote.origin.state_code,
        #             quote.destination.zip_code,
        #             quote.destination.name,
        #             quote.destination.state_code,
        #             quote.price,
        #             quote.date_est_ship,
        #             quote.status,
        #             quote.trailer_type,
        #             quote.condition,
        #             quote.source.name if quote.source else '',
        #             quote.user.username if quote.user else ''
        #         ])
        #
        # self.stdout.write(self.style.SUCCESS(f'Successfully exported data to {csv_file}'))
