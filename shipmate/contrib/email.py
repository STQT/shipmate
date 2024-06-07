import imaplib
import email
import logging
from email.header import decode_header
from dataclasses import dataclass
from typing import List

from django.core.mail import EmailMultiAlternatives
import os


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
                            charset = part.get_content_charset()
                            if charset:
                                body = part.get_payload(decode=True).decode(charset)
                            else:
                                # If charset is not specified, assume UTF-8
                                body = part.get_payload(decode=True).decode('utf-8', 'ignore')
                            break
                    emails.append(
                        EmailMessage(subject=subject,
                                     sender=sender,
                                     recipient=recipient,
                                     date=date,
                                     body=body))

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
    finally:
        # Logout and close connection
        imap.logout()

    return emails


def send_email(from_email, subject, to_emails, text_content=None, html_content=None, attachment=None):
    email = EmailMultiAlternatives(subject, text_content, from_email, to_emails)

    if html_content:
        email.attach_alternative(html_content, "text/html")

    if attachment and os.path.exists(attachment):
        with open(attachment, 'rb') as f:
            file_data = f.read()
        email.attach(os.path.basename(attachment), file_data)

    email.send()

# Example usage:
# subject = "Subject of the email"
# to_email = "leads@example.com"
# text_content = "Plain text content of the email"
# html_content = "<p>HTML content of the email</p>"
# attachment_path = "/path/to/your/attachment/file.pdf"

# send_email("gayratbek.sultonov@gmail.com",
#            subject, to_email,
#            text_content=text_content, html_content=html_content, attachment=attachment_path)
