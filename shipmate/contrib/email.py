import imaplib
import email
import logging
from email.header import decode_header
from dataclasses import dataclass
from typing import List, Optional

from django.core.mail import EmailMultiAlternatives, get_connection
import os


@dataclass
class EmailMessage:
    subject: str
    sender: str
    recipient: str
    date: str
    body: str


def fetch_emails(username, password, imap_server="imap.gmail.com", port=993) -> List[EmailMessage]:
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


def send_email(from_email, subject, to_emails, text_content=None, html_content=None, attachment=None, cc_emails=None,
               bcc_emails=None, host=None, user=None, password=None):
    # Set up the connection with custom settings if provided
    connection = get_connection(
        backend='django.core.mail.backends.smtp.EmailBackend',
        host=host,
        port=587,
        username=user,
        password=password,
        use_tls=True,

    ) if host and user and password else None

    # Create the email message
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=from_email,
        to=to_emails,
        cc=cc_emails,
        bcc=bcc_emails,
        connection=connection
    )

    # Attach HTML content if provided
    if html_content:
        email.attach_alternative(html_content, "text/html")

    # Attach a file if provided and exists
    if attachment and os.path.exists(attachment):
        with open(attachment, 'rb') as f:
            file_data = f.read()
        email.attach(os.path.basename(attachment), file_data)

    # Send the email
    email.send()


# Example usage:
# subject = "Subject of the email"
# to_email = "users@matelogisticss.com"
# text_content = "Plain text content of the email"
# html_content = "<p>HTML content of the email</p>"
# # attachment_path = "/path/to/your/attachment/file.pdf"
#
# send_email(from_email=to_email,
#            subject=subject, to_emails=['murodovazizmurod@gmail.com'],
#            text_content=text_content, html_content=html_content, host='smtp.sendgrid.net', user='apikey', password='')
