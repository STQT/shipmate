from shipmate.company_management.models import LeadParsingGroup, LeadParsingItem, LeadParsingValue

data_mapper = {
    '{customer.fullname}': 'customer__fullname',
    '{customer.name}': 'customer__name',
    '{customer.last_name}': 'customer__last_name',
    '{customer.phone}': 'customer__phone',
    '{customer.extra.phone}': 'customer__extra_phone',
    '{customer.email}': 'customer__email',

    '{origin.city}': 'origin__city',
    '{origin.state.name}': 'origin__state__name',
    '{origin.state.code}': 'origin__state__code',
    '{origin.zip}': 'origin__zip',
    '{destination.city}': 'destination__city',
    '{destination.state.name}': 'destination__state__name',
    '{destination.state.code}': 'destination__state__code',
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


text = """
Salom
Origin City: Gayrat Sultonov
How are you
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
    if field.startswith("vehicle"):
        vehicle, model_field = field.split("__")

    return get_value(text, value)


def parsing_email(text, ):
    values = LeadParsingValue.objects.all()
    data = {}
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
            data[field] = handle_special_fields(text, field, value)

# finding_text_original = "origin city:"
# value = get_value(text, finding_text_original)
