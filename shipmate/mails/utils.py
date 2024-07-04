from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from shipmate.addresses.models import City, States
from shipmate.cars.models import CarsModel, CarMarks
from shipmate.company_management.models import LeadParsingValue
from shipmate.contrib.models import ConditionChoices, TrailerTypeChoices
from shipmate.customers.models import Customer
from shipmate.lead_managements.models import Provider
from shipmate.leads.models import LeadVehicles, Leads

User = get_user_model()

data_mapper = {
    '{customer.fullname}': 'customer__name',
    '{customer.name}': 'customer__name',
    '{customer.last_name}': 'customer__last_name',
    '{customer.phone}': 'customer__phone',
    '{customer.extra.phone}': 'customer__extra_phone',
    '{customer.email}': 'customer__email',

    '{origin.city}': 'origin__city',
    '{origin.state.name}': 'origin__state_name',
    '{origin.state.code}': 'origin__state_code',
    '{origin.zip}': 'origin__zip',
    '{destination.city}': 'destination__city',
    '{destination.state.name}': 'destination__state_name',
    '{destination.state.code}': 'destination__state_code',
    '{destination.zip}': 'destination__zip',

    '{vehicle.year}': 'vehicle__year',
    '{vehicle.make}': 'vehicle__make',
    '{vehicle.model}': 'vehicle__model',
    '{vehicle.condition}': 'vehicle__condition',
    '{vehicle.vehicle_type}': 'vehicle__vehicle_type',
    '{vehicle.trailer_type}': 'vehicle__trailer_type',

    '{vehicle2.year}': 'vehicle2__year',
    '{vehicle2.make}': 'vehicle2__make',
    '{vehicle2.model}': 'vehicle2__model',
    '{vehicle2.condition}': 'vehicle2__condition',
    '{vehicle2.vehicle_type}': 'vehicle2__vehicle_type',
    '{vehicle2.trailer_type}': 'vehicle2__trailer_type',

    '{vehicle3.year}': 'vehicle3__year',
    '{vehicle3.make}': 'vehicle3__make',
    '{vehicle3.model}': 'vehicle3__model',
    '{vehicle3.condition}': 'vehicle3__condition',
    '{vehicle3.vehicle_type}': 'vehicle3__vehicle_type',
    '{vehicle3.trailer_type}': 'vehicle3__trailer_type',

    '{date_est_ship}': 'date_est_ship',
    '{notes}': 'notes'
}

# def parse_and_update_leads(original):
#     lines = original.strip().split('\n')
#     lead_data = {}
#     for value in LeadParsingValue.objects.all():
#
#         for line in lines:
#             # Split the line to separate the field placeholder and the value
#             ...
#
#     return lead_data


# text = """
#
#
# First Name: viviano
# Last Name: villarreal
# Email: viviano.v@gmail.com
# Phone: 8882309117
# Type: COUPE
# Year: 1985
# Make: MERCEDES-BENZ
# Model: 380SL
# Running Condition: Running
# Type Of Carrier: Open
# Vehicle #2 Type:
# Vehicle #2 Year:
# Vehicle #2 Make:
# Vehicle #2 Model:
# Vehicle #2 Running Condition:
# Vehicle #2 Type Of Carrier:
# Origin City: NEWARK
# Origin State: NJ
# Origin Zip: 07101
# Destination City: HOUSTON
# Destination State: TX
# Destination Zip: 77001
# Proposed Ship Date: 07/14/2024
# Comments:
# Requested On: 07/01/2024 05:37:05 AM
# ID:1379918
# """
text = """
First Name: Test 01
Last Name: Test
Email: test01@icloud.com <paigedpatrick@icloud.com>
Phone: (210) 862-3422
Type: Sedan Small
Year: 2007
Make: Toyota
Model: Prius
Running Condition: Running
Type Of Carrier: Enclosed
Vehicle #2 Type:
Vehicle #2 Year:
Vehicle #2 Make:
Vehicle #2 Model:
Vehicle #2 Running Condition:
Vehicle #2 Type Of Carrier:
Origin City: RICHMOND
Origin State: CA
Origin Zip: 94804
Destination City: AUSTIN
Destination State: TX
Destination Zip: 78713
Proposed Ship Date: 07/08/2024
Comments:
Requested On: 07/04/2024 07:00:59 AM
ID:1380659
"""


def finding_text(original, finding_text_original) -> int:
    lower_text = original.lower()
    lower_finding_text = finding_text_original.lower()
    finding_text_len = len(finding_text_original)
    num_index = lower_text.find(lower_finding_text)
    if num_index != -1:
        end_index = finding_text_len + num_index
        return end_index
    return num_index


def get_value(original, finding_text_original):
    num_index = finding_text(original, finding_text_original)
    if num_index == -1:
        return None
    start_line_index = original.rfind('\n', 0, num_index) + 1

    # Find the end of the line containing the found text
    end_line_index = original.find('\n', num_index)
    if end_line_index == -1:
        end_line_index = len(original)

    # Extract the line containing the found text
    line = original[start_line_index:end_line_index]

    # Extract the substring starting from num_index to the end of the line
    result = line[num_index - start_line_index:]

    return result.strip()


def handle_special_fields(text, field, value):
    # Add your custom logic to handle fields that start with "vehicle", "customer", "origin", or "destination"
    # For now, it will simply return the value after finding the specified text
    returned_value = get_value(text, value)
    if field.startswith("vehicle"):
        if not (field.startswith("vehicle2") or field.startswith("vehicle3")):
            # for only vehicle__field
            _vehicle, model_field = field.split("__")
            return returned_value, model_field, "vehicle1"
        elif field.startswith("vehicle2"):
            _vehicle, model_field = field.split("__")
            return returned_value, model_field, "vehicle2"
        else:
            _vehicle, model_field = field.split("__")
            return returned_value, model_field, "vehicle3"
    elif field.startswith("customer"):
        _customer, model_field = field.split("__")
        return returned_value, model_field, "customer"
    elif field.startswith("origin"):
        _origin, model_field = field.split("__")
        return returned_value, model_field, "origin"
    elif field.startswith("destination"):
        _destination, model_field = field.split("__")
        return returned_value, model_field, "destination"


def get_city(zip, state_code, city):
    city_qs = City.objects.filter(zip=zip.zfill(5))  # noqa
    if city_qs.exists():
        city_obj = city_qs.first()
    else:
        destination_state, _created = States.objects.get_or_create(
            code=state_code, defaults={"name": state_code})
        city_obj, _created = City.objects.get_or_create(
            zip=zip.zfill(5), defaults={"name": city, "state": destination_state}
        )
    return city_obj


def get_car_model(name, vehicle_type, mark_name):
    mark, _created = CarMarks.objects.get_or_create(name=mark_name.capitalize())
    model, _created = CarsModel.objects.get_or_create(mark=mark, name=name.capitalize(), vehicle_type=vehicle_type)
    return model


def parsing_email(text, email):
    print("START")
    data = {}
    values = LeadParsingValue.objects.all()
    # try:
    source = Provider.objects.get(email=email)
    # except Provider.DoesNotExist:
    #     return
    # TODO set user with logic prodiver exclusive user
    data["user"] = User.objects.get(pk=1)
    data["source"] = source
    vehicle1 = {}
    vehicle2 = {}
    vehicle3 = {}
    customer_data = {}
    origin_data = {}
    destination_data = {}

    for v in values:
        item = v.item.name
        value = v.value
        field = data_mapper[item]
        if not (
            field.startswith("vehicle") or field.startswith("customer") or field.startswith("origin") or
            field.startswith("destination")
        ):
            data[field] = get_value(text, value)
        else:
            returned_value, model_field, endpoint = handle_special_fields(text, field, value)
            if endpoint == "vehicle1":
                vehicle1[model_field] = returned_value
            elif endpoint == "vehicle2":
                vehicle2[model_field] = returned_value
            elif endpoint == "vehicle3":
                vehicle3[model_field] = returned_value
            elif endpoint == "customer":
                customer_data[model_field] = returned_value
            elif endpoint == "origin":
                origin_data[model_field] = returned_value
            elif endpoint == "destination":
                destination_data[model_field] = returned_value
    origin = get_city(origin_data['zip'], origin_data['state_code'], origin_data['city'])
    destination = get_city(destination_data['zip'],
                           destination_data['state_code'],
                           destination_data['city'])
    customer, _created = Customer.objects.get_or_create(email=customer_data.get('email',
                                                                                customer_data['phone'] + "@gmail.com"),
                                                        defaults=
                                                        {"phone": customer_data['phone'],
                                                         "name": customer_data['name'],
                                                         "last_name": customer_data['last_name']
                                                         }
                                                        )
    # try:
    data['date_est_ship'] = datetime.strptime(data['date_est_ship'], "%m/%d/%Y")
    # except ValidationError:
    #     try:
    #         data['date_est_ship'] = datetime.strptime(data['date_est_ship'], "%m-%d-%Y")
    #     except ValidationError:
    #         data['date_est_ship'] = datetime.strptime(data['date_est_ship'], "%Y/%m/%d")
    lead = Leads.objects.create(
        customer=customer,
        origin=origin,
        destination=destination,
        condition=ConditionChoices.DRIVES if vehicle1['condition'] == "Running" else ConditionChoices.ROLLS,
        trailer_type=TrailerTypeChoices.OPEN if vehicle1['trailer_type'] == "Open" else TrailerTypeChoices.CLOSE,
        **data)
    car_model = get_car_model(vehicle1['model'], vehicle1['vehicle_type'], vehicle1['make'])
    LeadVehicles.objects.create(lead=lead, vehicle=car_model, vehicle_year=vehicle1['year'])
    if vehicle2:
        car_model = get_car_model(vehicle2['model'], vehicle2['vehicle_type'], vehicle2['make'])
        LeadVehicles.objects.create(lead=lead, vehicle=car_model, vehicle_year=vehicle2['year'])
    if vehicle3:
        car_model = get_car_model(vehicle3['model'], vehicle3['vehicle_type'], vehicle3['make'])
        LeadVehicles.objects.create(lead=lead, vehicle=car_model, vehicle_year=vehicle3['year'])
