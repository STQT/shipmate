import imaplib
import email
from email.header import decode_header
from dataclasses import dataclass
from typing import List

from django.conf import settings


@dataclass
class EmailMessage:
    subject: str
    sender: str
    recipient: str
    date: str
    body: str


def fetch_emails(username, password, imap_server="imap.example.com", port=993) -> List[EmailMessage]:
    emails = []

    try:
        # Connect to the IMAP server
        imap = imaplib.IMAP4_SSL(imap_server, port)
        imap.login(username, password)
        imap.select("INBOX")  # Select the mailbox you want to listen to

        # Search for unseen emails
        status, response = imap.search(None, "(UNSEEN)")

        if status == "OK":
            for num in response[0].split():
                status, data = imap.fetch(num, "(RFC822)")
                if status == "OK":
                    raw_email = data[0][1]
                    email_message = email.message_from_bytes(raw_email)
                    subject = decode_header(email_message["Subject"])[0][0]
                    if isinstance(subject, bytes):
                        subject = subject.decode()
                    sender = email_message["From"]
                    recipient = email_message["To"]
                    date = email_message["Date"]
                    body = ""
                    # Process email body as needed
                    for part in email_message.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode(part.get_content_charset())
                            break
                    emails.append(EmailMessage(subject, sender, recipient, date, body))

    except Exception as e:
        print("An error occurred:", str(e))
    finally:
        # Logout and close connection
        imap.logout()

    return emails


# Example usage:
# username = settings.IMAP_EMAIL_USER
# password = settings.IMAP_EMAIL_PASSWORD
# emails = fetch_emails(username, password, imap_server="imap.gmail.com")
# for email in emails:
#     print(email)
