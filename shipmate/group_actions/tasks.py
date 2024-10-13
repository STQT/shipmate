import re
import time

from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model

from shipmate.contrib.email import send_email
from shipmate.contrib.models import Attachments
from shipmate.contrib.sms import send_sms
from shipmate.group_actions.utils import ATTACHMENT_ATTACHMENT_MAP, ATTACHMENT_FK_FIELD_MAP, ATTACHMENT_CLASS_MAP

User = get_user_model()


@shared_task
def send_sms_task(user_id, ids, endpoint_type, message):
    print('active')
    user = User.objects.get(pk=user_id)  # noqa
    model_class = ATTACHMENT_CLASS_MAP[endpoint_type]
    fk_field = ATTACHMENT_FK_FIELD_MAP[endpoint_type]
    attachment_class = ATTACHMENT_ATTACHMENT_MAP[endpoint_type]

    objs = model_class.objects.filter(id__in=ids).select_related("customer")
    phones = []
    for obj in objs:
        data = {
            fk_field: obj,
            "title": f'Sent sms from {user.first_name} to {obj.customer.phone}',
            "user": user,
            "second_title": f'Message: {message}',
            "type": Attachments.TypesChoices.PHONE,
            "link": 0
        }
        phones.append(obj.customer.phone)
        attachment_class.objects.create(**data)
    CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

    message = re.sub(CLEANR, '', message)
    for phone in phones:
        send_sms(user.phone, [phone], message)
        time.sleep(1)


@shared_task
def send_email_task(user_id, ids, endpoint_type, message, subject="", cc_list=None, bcc_emails=None):
    user = User.objects.get(pk=user_id)  # noqa
    model_class = ATTACHMENT_CLASS_MAP[endpoint_type]
    fk_field = ATTACHMENT_FK_FIELD_MAP[endpoint_type]
    attachment_class = ATTACHMENT_ATTACHMENT_MAP[endpoint_type]

    objs = model_class.objects.filter(id__in=ids).select_related("customer")
    email_list = []
    for obj in objs:
        data = {
            fk_field: obj,
            "title": f'Sent email from {user.first_name} to {obj.customer.email}',
            "user": user,
            "second_title": f'Email: {message}',
            "type": Attachments.TypesChoices.EMAIL,
            "link": 0
        }
        try:
            attachment_class.objects.create(**data)
            send_email(subject=subject, text_content=message, from_email=user.email,
                       to_emails=[obj.customer.email], bcc_emails=bcc_emails, cc_emails=cc_list, host='smtp.sendgrid.net',
                       user='apikey',
                       password=settings.SENDGRID_API_KEY)
            # email_list.append(obj.customer.email)
        except Exception as e:
            print(e)
            continue
