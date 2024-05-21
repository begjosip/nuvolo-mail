import logging
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


class EmailService:
    def __init__(self):
        self._smtp_server = os.getenv("SMTP_SERVER")
        self._smtp_port = os.getenv("SMTP_PORT")
        self._smtp_mail = os.getenv("SMTP_APP_MAIL")
        self._smtp_password = os.getenv("SMTP_PASSWORD")
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def send_verification_email(verification):
        print("Sending email to:")
    #     TODO:

    @staticmethod
    def send_pass_reset_email(pass_reset):
        print("Sending email to:")
    #     TODO:

    @staticmethod
    def send_notification_email(notification):
        print("Sending email to:")
    #     TODO: