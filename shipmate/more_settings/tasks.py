import re

from celery import shared_task

from config import settings
from shipmate.contrib.email import send_email
from shipmate.contrib.sms import send_sms  # Assuming you're using a service for SMS
from shipmate.more_settings.models import Automation
from django.conf import settings



@shared_task
def send_automation_message(customer_email, user_phone, customer_phone, automation_id):
    try:
        automation = Automation.objects.get(id=automation_id)

        if automation.email_template and automation.email_template.template_type == "email":
            from_email=settings.DEFAULT_FROM_EMAIL  # Your email address
            send_email(
                from_email=from_email,
                subject=automation.email_template.subject if automation.email_template.subject else 'Subject Test',
                text_content=automation.email_template.body,  # email content
                to_emails=[customer_email]
            )

        if automation.sms_template and automation.sms_template.template_type == "sms":
            CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

            text = re.sub(CLEANR, '', automation.sms_template.body)
            send_sms(
                from_email=user_phone,
                to_numbers=[customer_phone],
                message=text  # SMS content
            )
    except Automation.DoesNotExist:
        print(f"Automation with id {automation_id} not found.")
