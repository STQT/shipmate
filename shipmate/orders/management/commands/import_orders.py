import csv
import json

from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from shipmate.cars.models import CarsModel, CarMarks
from shipmate.contrib.db import update_sequences
from shipmate.orders.models import Order, OrderVehicles
from shipmate.quotes.models import Quote, QuoteVehicles, QuoteDates
from shipmate.contrib.models import OrderStatusChoices, QuoteStatusChoices, TrailerTypeChoices, ConditionChoices
from shipmate.addresses.models import City, States
from shipmate.customers.models import Customer
from shipmate.lead_managements.models import Provider

User = get_user_model()

DEFAULT_ESTIMATED_SHIP_DATE = "01-06-2024"


def read_csv(filename):
    with open(filename, newline='') as csvfile:
        csvreader = csv.reader(csvfile, quotechar='"', delimiter=',')
        # Read the header
        header = next(csvreader)
        # Get the expected number of fields based on the header
        expected_num_fields = len(header)
        # Read the rest of the data, skipping rows with double delimiters
        data = []
        for row in csvreader:
            # Check if the row contains the expected number of fields
            if len(row) == expected_num_fields:
                data.append(row)
            else:
                print(f"Skipping row due to incorrect number of fields: {row}")
    return header, data


# username_mapper = {
#     'Addison.oblog': 'info@oceanbluego.com',
#     'Grace.oblog': 'grace@oceanbluego.com',
#     'John.oblog': 'john@oceanbluego.com',
#     'Michael.oblog': 'info@oceanbluego.com',
#     'Dina.oblog': 'info@oceanbluego.com',
#     '\\N': 'info@oceanbluego.com',
#     '': 'info@oceanbluego.com',
#     'Albert.mob': 'info@oceanbluego.com',
#     'Anne.oblog': 'info@oceanbluego.com',
#     'Mike.oblog': 'info@oceanbluego.com',
#     'Steve': 'info@oceanbluego.com',
#     'Sam': 'info@oceanbluego.com',
#     'developer': 'info@oceanbluego.com',
#     'Frank.oblog': 'info@oceanbluego.com',
#     'Jane.oblog': 'info@oceanbluego.com',
#     'Kevin.oblog': 'info@oceanbluego.com',
#     'Leo.oblog': 'info@oceanbluego.com',
#     'Lucas.oblog': 'info@oceanbluego.com'
# }


username_mapper = {
    'Ronald.matelog': 'Ronald@gmail.com',
    'Scott.matelog': 'scott@matelogisticss.com',
    'developer': 'brian@matelogisticss.com',
    'James.matelog': 'brian@matelogisticss.com',
    '\\N': 'brian@matelogisticss.com',
    'Daniel.matelog': 'daniel@matelogisticss.com',
    'Tony.matelog': 'brian@matelogisticss.com',
    'Rachael.matelog': 'brian@matelogisticss.com',
    'Richard.matelog': 'brian@matelogisticss.com',
    'Ali.matelog': 'brian@matelogisticss.com',
    'Patrick.matelog': 'brian@matelogisticss.com',
    'Sean.matelog': 'brian@matelogisticss.com',
    'Ben.matelog': 'brian@matelogisticss.com',
    'Michael.matelog': 'brian@matelogisticss.com',
    'Zia.matelog': 'brian@matelogisticss.com',
}

QUOTE_MAPPER = {
    "2": QuoteStatusChoices.FOLLOWUP,  # noqa
    "3": QuoteStatusChoices.ARCHIVED,  # noqa
    "21": QuoteStatusChoices.ONHOLD  # noqa
}

ORDER_MAPPER = {
    "4": OrderStatusChoices.ORDERS,
    "7": OrderStatusChoices.POSTED,
    "8": OrderStatusChoices.DISPATCHED,
    "9": OrderStatusChoices.ONHOLD,
    "10": OrderStatusChoices.COMPLETED,
    "11": OrderStatusChoices.COMPLETED,  # noqa
    "12": OrderStatusChoices.ARCHIVED,  # noqa
    "13": OrderStatusChoices.ARCHIVED,  # noqa
    "60": OrderStatusChoices.BOOKED,  # noqa
    "61": OrderStatusChoices.ARCHIVED,
    "80": OrderStatusChoices.NOTSIGNED,
    "81": OrderStatusChoices.PICKEDUP

}
SHIP_VIA_ID = {
    "1": TrailerTypeChoices.OPEN,
    "2": TrailerTypeChoices.CLOSE,
    "3": TrailerTypeChoices.OPEN
}

quote_status_list = ["2", "3", "21"]
order_status_list = ["4", "7", "8", "9", "10", "11", "12", "13", "60", "61", "80", "81"]

c = []


class Command(BaseCommand):
    help = 'Import CSV data to DB'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        json_file_path = kwargs['csv_file']  # noqa
        header, data = read_csv(json_file_path)
        for num, row in enumerate(data):
            date_entered: datetime = datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")  # "%Y-%m-%d %H:%M:%S"
            phone: str = row[2]  # 2395608470
            email: str = row[3]  # amkania@yahoo.com
            if not email:
                continue
            print(num, phone)
            first_name: str = row[4]  # Andrea
            last_name: str = row[5]  # Kania
            """
            [{"id":"0","year":"2013","model":"4Runner","make":"Toyota","type":"SUV","recommended_price":"0.00",
            "deposit":"200","total":"1950"}]
            """
            vehicles_str: str = row[6]
            vehicles: list[dict] = json.loads(vehicles_str)
            pickup_zip: str = row[7][:5] if row[7][:5].isdigit() else "00000"  # 95014
            pickup_zip = pickup_zip.zfill(5)
            pickup_city: str = row[8].capitalize()  # CUPERTINO
            pickup_state_code: str = row[9]  # CA
            dropoff_zip: str = row[10][:5] if row[10][:5].isdigit() else "00000"  # 76134
            dropoff_zip = dropoff_zip.zfill(5)
            dropoff_city: str = row[11].capitalize() if len(row[11]) < 100 else "None"  # FORTWORTH
            dropoff_state_code: str = row[12]  # TX
            price_total_total = row[13]
            if price_total_total == "NaN":
                price_total_total = vehicles[0]["total"]
                if not price_total_total or not price_total_total.isdigit():
                    price_total_total = "0"
            try:
                price_total_total = int(float(price_total_total))
            except ValueError:
                price_total_total = 0
            if row[14] == "\\N" or len(row[14]) > 10:
                estimated_ship_date = DEFAULT_ESTIMATED_SHIP_DATE
            else:
                estimated_ship_date = row[14]  # 28/06/2022
            try:
                estimated_ship_date_obj: datetime.date = datetime.strptime(
                    estimated_ship_date, "%d/%m/%Y").date()
            except ValueError:
                estimated_ship_date_obj: datetime.date = datetime.strptime(
                    DEFAULT_ESTIMATED_SHIP_DATE, "%d-%m-%Y").date()
            print(row[7])
            print(row[8])
            lead_status: str = row[15]  # 9
            ship_via_id: str = SHIP_VIA_ID[row[16]]
            vehicle_runs: str = ConditionChoices.ROLLS if row[17] == "0" else ConditionChoices.DRIVES  # 9
            provider_name: str = row[18]  # 9
            provider_obj, _created = Provider.objects.get_or_create(
                name=provider_name, defaults={
                    "type": "standard",
                    "effective": "no",
                    "email": provider_name + "@email.com",
                    "subject": provider_name + " " + provider_name
                }
            )
            try:
                user_name: str = row[20]
            except IndexError:
                user_name: str = "Ali.matelog"  # "Addison.oblog"
            if not user_name:
                user_name: str = "Ali.matelog"
            user_email_str: str = username_mapper[user_name]
            user, _created = User.objects.get_or_create(
                email=user_email_str, defaults={
                    'first_name': user_name,
                    'last_name': last_name,
                    'phone': phone,
                }
            )
            customer, _created = Customer.objects.get_or_create(
                email=email, defaults={'name': first_name, "last_name": last_name, 'phone': phone}
            )
            origin = City.objects.filter(zip=pickup_zip)  # noqa
            if origin.exists():
                origin = origin.first()
            else:
                origin_state = States.objects.filter(code=pickup_state_code).first()
                if not origin_state:
                    origin_state, _created = States.objects.get_or_create(code="ZZ", defaults={"name": "No name"})
                    pickup_city = "No name"
                    pickup_zip = "00000"
                origin, _created = City.objects.get_or_create(
                    zip=pickup_zip, defaults={"name": pickup_city, "state": origin_state}
                )

            destination = City.objects.filter(zip=dropoff_zip)  # noqa
            if destination.exists():
                destination = destination.first()
            else:

                destination_state, _created = States.objects.get_or_create(
                    code=dropoff_state_code, defaults={"name": dropoff_state_code})
                destination, _created = City.objects.get_or_create(
                    zip=dropoff_zip, defaults={"name": dropoff_city, "state": destination_state}
                )
            c.append(lead_status)
            reservation_price = vehicles[0]['deposit'] if vehicles else 0
            if not reservation_price or not reservation_price.isdigit():
                reservation_price = 0

            if lead_status in quote_status_list:
                # QUOTE
                try:
                    quote = Quote.objects.create(
                        created_at=date_entered,
                        updated_at=date_entered,
                        status=QUOTE_MAPPER[lead_status],
                        price=price_total_total,
                        reservation_price=reservation_price,
                        customer=customer,
                        date_est_ship=estimated_ship_date_obj,
                        source=provider_obj,
                        user=user,
                        origin=origin,
                        destination=destination,
                        trailer_type=ship_via_id,
                        condition=vehicle_runs,
                    )
                    QuoteDates.objects.get_or_create(quote=quote, defaults={
                        "quoted": date_entered
                    })
                except Exception as e:
                    print(f"Exceptioned quote: {e} {e.args}", row)
                    continue
                self.add_vehicles(vehicles, QuoteVehicles, "quote", quote)
                self.stdout.write(self.style.SUCCESS('Finished creating quote'))
            elif lead_status in order_status_list:
                # ORDER
                try:
                    order = Order.objects.create(
                        created_at=date_entered,
                        price=price_total_total,
                        reservation_price=reservation_price,
                        date_est_ship=estimated_ship_date_obj,
                        customer=customer,
                        user=user,
                        origin=origin,
                        destination=destination,
                        status=ORDER_MAPPER[lead_status],
                        trailer_type=ship_via_id,
                        condition=vehicle_runs,
                        source=provider_obj
                    )
                except Exception as e:
                    print(f"Exceptioned order: {e} {e.args}", row)
                    continue
                self.add_vehicles(vehicles, OrderVehicles, "order", order)
                self.stdout.write(self.style.SUCCESS('Finished creating order'))
            else:
                print(row, "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print("lead_status: ", lead_status)
                break
            # except Exception as e:
            #     print(f"Exceptioned: {e} {e.args}", row)
            #     continue

        self.update_used_sequences()
        self.stdout.write(self.style.SUCCESS('Finished creating orders | quotes'))

    def add_vehicles(self, vehicles, klass, field, rel):
        for vehicle in vehicles:
            vehicle_year = vehicle['year']
            if not vehicle_year or not vehicle_year.isdigit() or int(vehicle_year) > 3000:
                vehicle_year = 2024

            car_mark, _created = CarMarks.objects.get_or_create(
                name=vehicle['make'].capitalize(), defaults={"is_active": True}
            )
            car_model, _created = CarsModel.objects.get_or_create(
                mark=car_mark,
                name=vehicle['model'].capitalize(), vehicle_type=vehicle['type'])
            vehicle_data = {
                field: rel,
                "vehicle_year": vehicle_year,
                "vehicle": car_model
            }
            klass.objects.create(**vehicle_data)

    def update_used_sequences(self):
        update_sequences(City, 'addresses_city_id_seq')
        update_sequences(States, 'addresses_states_id_seq')
        update_sequences(QuoteVehicles, 'quotes_quotevehicles_id_seq')
        update_sequences(Quote, 'quotes_quote_id_seq')
        update_sequences(Order, 'orders_order_id_seq')
        update_sequences(OrderVehicles, 'orders_ordervehicles_id_seq')
        update_sequences(CarsModel, 'cars_carsmodel_id_seq')
        update_sequences(CarMarks, 'cars_carmarks_id_seq')
