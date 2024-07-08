import email as email_lib
from django.core.management.base import BaseCommand

from shipmate.mails.models import Mail
from shipmate.mails.utils import parsing_email


class Command(BaseCommand):
    help = 'Import mails using Mail model'

    def add_arguments(self, parser):
        parser.add_argument('start_id', type=str, help='The path to the start ID')

    def handle(self, *args, **kwargs):
        start_id = kwargs['start_id']
        for i in Mail.objects.filter(pk__gt=start_id):
            sender_email = email_lib.utils.parseaddr(i.sender)[1]
            parsing_email(i.body, sender_email, subject=i.subject)

        self.stdout.write(self.style.SUCCESS(f'Successfully exported data to {start_id}'))
