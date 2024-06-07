import requests
from django.conf import settings

# Replace with your actual API key
DIALPAD_API_KEY = settings.DIALPAD_API_KEY

# Dialpad API endpoint for sending SMS
DIALPAD_SMS_ENDPOINT = 'https://dialpad.com/api/v2/sms'


def send_sms(from_number, to_number, message):
    headers = {
        'Authorization': f'Bearer {DIALPAD_API_KEY}',
        'Content-Type': 'application/json',
    }

    payload = {
        'from_number': from_number,
        'to_numbers': to_number,
        'text': message
    }

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
