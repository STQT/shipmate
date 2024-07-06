from django.core.mail import send_mail
from django.conf import settings

from shipmate.company_management.models import CompanyInfo
from shipmate.orders.models import OrderContract


def send_order_contract_email(order_contract: OrderContract):
    company = CompanyInfo.objects.first()
    company_name = company.name
    contact_email = company.email
    contact_mainline = company.mainline
    subject = 'New Order Contract Created'
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
{order_contract.order.user.name}
{company_name}
{contact_email}
{contact_mainline}
"""
    from_email = settings.EMAIL_HOST_USER  # Your email address
    password_email = settings.EMAIL_HOST_PASSWORD
    recipient_list = [order_contract.order.customer.email]  # List of recipients

    send_mail(subject, message, from_email, recipient_list, auth_user=from_email, auth_password=password_email)
