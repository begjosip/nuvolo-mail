import logging
import os
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Template


class EmailService:
    VERIFICATION_TEMPLATE_PATH = 'templates/verification.html'
    NOTIFICATION_TEMPLATE_PATH = 'templates/notification.html'
    PASSWORD_RESET_TEMPLATE_PATH = 'templates/password_reset_request.html'
    LOGO_IMAGE_PATH = 'templates/images/nuvolo.png'

    def __init__(self):
        self._smtp_server = os.getenv("SMTP_SERVER")
        self._smtp_port = os.getenv("SMTP_PORT")
        self._smtp_mail = os.getenv("SMTP_APP_MAIL")
        self._smtp_password = os.getenv("SMTP_PASSWORD")
        self.logger = logging.getLogger(__name__)

    def send_verification_email(self, verification):
        self.logger.info("Fetching template for verification")
        with open(self.VERIFICATION_TEMPLATE_PATH, 'r') as file:
            template = Template(file.read())
        html_body = template.render({
            'name': verification.firstName + ' ' + verification.lastName,
            'verification_link': os.getenv("VERIFICATION_URI") + verification.token
        })
        msg = MIMEMultipart('related')
        msg['From'] = self._smtp_mail
        msg['To'] = verification.email
        msg['Subject'] = 'Verify your account'
        msg.attach(MIMEText(html_body, 'html'))
        with open(self.LOGO_IMAGE_PATH, 'rb') as img_file:
            img = MIMEImage(img_file.read())
            img.add_header('Content-ID', '<nuvolo>')
            img.add_header('Content-Disposition', 'inline',
                           filename=os.path.basename(self.LOGO_IMAGE_PATH))
            msg.attach(img)
            self.logger.debug("Logging to SMTP server")
            server = smtplib.SMTP_SSL(self._smtp_server, int(self._smtp_port))
            server.login(self._smtp_mail, self._smtp_password)
            server.sendmail(self._smtp_mail, verification.email, msg.as_string())
            self.logger.info("Successfully sent email to {}", verification.email)
            server.quit()

    def send_pass_reset_email(self, pass_reset):
        self.logger.info("Fetching template for password reset email")
        with open(self.PASSWORD_RESET_TEMPLATE_PATH, 'r') as file:
            template = Template(file.read())
        html_body = template.render({
            'name': pass_reset.firstName + ' ' + pass_reset.lastName,
            'pass_reset_link': os.getenv("PASS_RESET_URI") + pass_reset.token
        })
        msg = MIMEMultipart('related')
        msg['From'] = self._smtp_mail
        msg['To'] = pass_reset.email
        msg['Subject'] = 'Forgot your password. No problem!'
        msg.attach(MIMEText(html_body, 'html'))
        with open(self.LOGO_IMAGE_PATH, 'rb') as img_file:
            img = MIMEImage(img_file.read())
            img.add_header('Content-ID', '<nuvolo>')
            img.add_header('Content-Disposition', 'inline',
                           filename=os.path.basename(self.LOGO_IMAGE_PATH))
            msg.attach(img)
            self.logger.debug("Logging to SMTP server")
            server = smtplib.SMTP_SSL(self._smtp_server, int(self._smtp_port))
            server.login(self._smtp_mail, self._smtp_password)
            server.sendmail(self._smtp_mail, pass_reset.email, msg.as_string())
            self.logger.info("Successfully sent email to {}", pass_reset.email)
            server.quit()

    def send_notification_email(self, notification):
        self.logger.info("Fetching template for verification")
        with open(self.VERIFICATION_TEMPLATE_PATH, 'r') as file:
            template = Template(file.read())
        html_body = template.render({
            'name': notification.firstName + ' ' + notification.lastName,
            'main_page_url': os.getenv("MAIN_PAGE_URI"),
            'message': notification.message
        })
        msg = MIMEMultipart('related')
        msg['From'] = self._smtp_mail
        msg['To'] = notification.email
        msg['Subject'] = 'Verify your account'
        msg.attach(MIMEText(html_body, 'html'))
        with open(self.LOGO_IMAGE_PATH, 'rb') as img_file:
            img = MIMEImage(img_file.read())
            img.add_header('Content-ID', '<nuvolo>')
            img.add_header('Content-Disposition', 'inline',
                           filename=os.path.basename(self.LOGO_IMAGE_PATH))
            msg.attach(img)
            self.logger.debug("Logging to SMTP server")
            server = smtplib.SMTP_SSL(self._smtp_server, int(self._smtp_port))
            server.login(self._smtp_mail, self._smtp_password)
            server.sendmail(self._smtp_mail, notification.email, msg.as_string())
            self.logger.info("Successfully sent email to {}", notification.email)
            server.quit()
