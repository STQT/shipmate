from celery import shared_task
from django.conf import settings

from shipmate.contrib.email import fetch_emails
from shipmate.mails.models import Mail


@shared_task
def fetch_emails_task():
    if settings.DEBUG is False:
        username = settings.IMAP_EMAIL_USER
        password = settings.IMAP_EMAIL_PASSWORD
        emails = fetch_emails(username, password, imap_server="imap.gmail.com")
        for email in emails:
            data = {
                'subject': email.subject,
                'sender': email.sender,
                'recipient': email.recipient,
                'date': email.date,
                'body': email.body,
            }
            Mail.objects.create(**data)
