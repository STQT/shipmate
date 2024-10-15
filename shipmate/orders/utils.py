from shipmate.contrib.email import send_email
from django.conf import settings

from shipmate.company_management.models import CompanyInfo
from shipmate.orders.models import OrderContract, Order
from shipmate.payments.models import OrderPayment, TypeChoices


def get_company_data():
    company = CompanyInfo.objects.first()
    company_name = company.name
    contact_email = company.email
    contact_mainline = company.mainline
    return company_name, contact_email, contact_mainline


def send_order_contract_email(order_contract: OrderContract):
    subject = 'New Order Contract Created'
    company_name, contact_email, contact_mainline = get_company_data()
    message = f"""Dear {order_contract.order.customer.name} {order_contract.order.customer.last_name},

Please find attached the electronic agreement for your review and signature. This agreement outlines the terms and conditions.

To sign the contract, please follow these steps:
 1. Click here to open the attached document.
 {settings.FRONTEND_URL}/contract/{order_contract.order.guid}/{order_contract.pk}
 2. Review all the details carefully.
 3. Sign electronically where indicated.
 4. The signed document will be emailed to you.
 5. Pay the reservation fee online from “Pay” button.
 6. Congratulations! You will be contacted when the driver is confirmed.

Should you have any questions or require any clarifications regarding the contract, please do not hesitate to contact us. We are here to assist you.

Thank you for your prompt attention to this matter. We look forward to receiving the signed contract at your earliest convenience.

Best regards,
{order_contract.order.user.first_name} {order_contract.order.user.last_name}
{company_name}
{contact_email}
{contact_mainline}
"""
    from_email = 'e-sign@connectacrm.com'  # Your email address
    password_email = settings.SIGN_EMAIL_PASSWORD
    recipient_list = [order_contract.order.customer.email]  # List of recipients

    send_email(subject=subject, text_content=message, from_email=from_email,
               to_emails=recipient_list, host='smtp.sendgrid.net', user='apikey', password=settings.CONNECTA_API)


def send_cc_agreement(order: Order, payment: OrderPayment, payment_id: int):
    company_name, contact_email, contact_mainline = get_company_data()
    url = f"{settings.FRONTEND_URL}/contract/pay/{order.guid}"
    if payment.payment_type == TypeChoices.credit_card:
        url = f"{settings.FRONTEND_URL}/contract/cc-auth/{order.guid}/{payment_id}"
    subject = "Action Required: Credit Card Authorization Form"
    message = f"""Dear {order.customer.name} {order.customer.last_name},

As part of our process to finalize your transaction, we kindly request that you complete the attached Credit Card Authorization Form. Please follow these steps:

1. Click here to fill out the online Credit Card Authorization Form completely and accurately.
{url}
2. Attach a clear image of both the front and back of the credit card.
3. Ensure that the name on the credit card matches the name on the contract.

This process helps us ensure the security and accuracy of your payment information.

If you have any questions or need assistance, feel free to contact us.

Thank you for your prompt attention to this matter.

Best regards,

{order.user.first_name} {order.user.last_name}
{company_name}
{contact_email}
{contact_mainline}
"""
    from_email = 'e-sign@connectacrm.com'  # Your email address
    password_email = settings.SIGN_EMAIL_PASSWORD
    recipient_list = [order.customer.email]  # List of recipients
    cc_list = [settings.CC_EMAIL]
    send_email(subject=subject, text_content=message, from_email=from_email, to_emails=recipient_list,
               cc_emails=cc_list, host='smtp.sendgrid.net', user='apikey', password=settings.CONNECTA_API)
