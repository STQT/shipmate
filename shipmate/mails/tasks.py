import email as email_lib
from celery import shared_task
from django.conf import settings

from shipmate.contrib.email import fetch_emails
from shipmate.mails.models import Mail
from shipmate.mails.utils import parsing_email


@shared_task
def fetch_emails_task():
    if settings.DEBUG is False:
        username = settings.IMAP_EMAIL_USER
        password = settings.IMAP_EMAIL_PASSWORD
        emails = fetch_emails(username, password, imap_server="imap.gmail.com")
        print(emails, username, password, '#####################################')
        for email in emails:
            data = {
                'subject': email.subject,
                'sender': email.sender,
                'recipient': email.recipient,
                'date': email.date,
                'body': email.body,
            }
            sender_email = email_lib.utils.parseaddr(email.sender)[1]
            print(data)
            Mail.objects.create(**data)
            parsing_email(email.body, sender_email, subject=email.subject)
