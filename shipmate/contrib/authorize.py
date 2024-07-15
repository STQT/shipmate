import json

import requests

from ..company_management.models import Merchant, MerchantTypeChoices

URL = "https://api2.authorize.net/xml/v1/request.api"


def get_authorize_credentials():
    merchant = Merchant.objects.filter(merchant_type=MerchantTypeChoices.AUTHORIZE).first()
    if merchant:
        return merchant.authorize_login, merchant.authorize_password
    else:
        raise Exception("No merchant credentials for authorize.net")


def charge_payment(amount, card_number, expiration_date, card_code):
    headers = {'Content-Type': 'application/json'}

    login_id, transaction_key = get_authorize_credentials()
    payload = {
        "createTransactionRequest": {
            "merchantAuthentication": {
                "name": login_id,
                "transactionKey": transaction_key
            },
            "transactionRequest": {
                "transactionType": "authCaptureTransaction",
                "amount": str(amount),
                "payment": {
                    "creditCard": {
                        "cardNumber": card_number,
                        "expirationDate": expiration_date,
                        "cardCode": card_code
                    }
                }
            }
        }
    }
    response = requests.post(URL, headers=headers, data=json.dumps(payload))
    return handle_response(response)


def refund_payment(amount, transaction_id, card_number, expiration_date):
    headers = {'Content-Type': 'application/json'}
    login_id, transaction_key = get_authorize_credentials()
    payload = {
        "createTransactionRequest": {
            "merchantAuthentication": {
                "name": login_id,
                "transactionKey": transaction_key
            },
            "transactionRequest": {
                "transactionType": "refundTransaction",
                "amount": str(amount),
                "payment": {
                    "creditCard": {
                        "cardNumber": card_number,
                        "expirationDate": expiration_date
                    }
                },
                "refTransId": transaction_id
            }
        }
    }
    response = requests.post(URL, headers=headers, data=json.dumps(payload))
    return handle_response(response)


def sent_payment(amount, card_number, expiration_date, card_code):
    # Assuming 'sent' transaction is similar to 'charge'
    return charge_payment(amount, card_number, expiration_date, card_code)


def tip_payment(original_amount, tip_amount, card_number, expiration_date, card_code):
    total_amount = original_amount + tip_amount
    return charge_payment(total_amount, card_number, expiration_date, card_code)


def handle_response(response):
    try:
        response_data = response.content.decode('utf-8-sig')
        response_json = json.loads(response_data)

        if response.status_code == 200:
            if response_json.get('messages', {}).get('resultCode') == "Ok":
                if 'transactionResponse' in response_json and 'messages' in response_json['transactionResponse']:
                    try:
                        transaction_id = response_json['transactionResponse']['transId']
                    except KeyError:
                        transaction_id = "None"
                    return {
                        "success": True,
                        "message": "Transaction successful.",
                        "transaction_id": transaction_id
                    }
                else:
                    return {
                        "success": False,
                        "message": response_json['transactionResponse']['errors']['error'][0]['errorText']
                    }
            else:
                return {
                    "success": False,
                    "message": response_json['messages']['message'][0]['text']
                }
        else:
            return {
                "success": False,
                "message": "Invalid response from Authorize.Net"
            }
    except json.JSONDecodeError:
        return {
            "success": False,
            "message": "Failed to decode JSON response from Authorize.Net"
        }
