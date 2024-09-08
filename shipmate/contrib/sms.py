import requests
import phonenumbers

from django.conf import settings

# Replace with your actual API key
DIALPAD_API_KEY = settings.DIALPAD_API_KEY

# Dialpad API endpoint for sending SMS
DIALPAD_SMS_ENDPOINT = 'https://dialpad.com/api/v2/sms'


def convert_to_e164(phone_number, country_code='US'):
    parsed_number = phonenumbers.parse(phone_number, country_code)
    e164_format = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
    return e164_format


def send_sms(from_email, to_numbers: list, message):
    headers = {
        'Authorization': f'Bearer {DIALPAD_API_KEY}',
        'Content-Type': 'application/json',
    }
    formatted_numbers = [convert_to_e164(number) for number in to_numbers]
    formatted_numbers = list(set(formatted_numbers))
    payload = {
        'from_number': from_email,
        'to_numbers': formatted_numbers,
        'text': message
    }
    print(payload)

    response = requests.post(DIALPAD_SMS_ENDPOINT, headers=headers, json=payload)

    if response.status_code == 200:
        print('SMS sent successfully!')
    else:
        print(f'Failed to send SMS. Status code: {response.status_code}, Response: {response.text}')

# Example usage
# from_number = '+19294061515'
# to_numbers = ['+19732459373']
# message = 'Hello, this is a test message from Dialpad!'
#
# send_sms(from_number, to_numbers, message)
