import pika
import json
import os
import logging

from email_service.email_service import EmailService


class RabbitMQListener:
    def __init__(self):
        self._credentials = pika.PlainCredentials(os.getenv("RABBITMQ_USER"), os.getenv("RABBITMQ_PASSWORD"))
        self._parameters = pika.ConnectionParameters(host=os.getenv("RABBITMQ_HOST"), port=os.getenv("RABBITMQ_PORT"),
                                                     credentials=self._credentials)
        self._connection = pika.BlockingConnection(self._parameters)
        self._channel = self._connection.channel()
        self.logger = logging.getLogger(__name__)
        self._email_service = EmailService()

    def start_listening(self):
        self._channel.basic_qos(prefetch_count=1)
        self._channel.basic_consume(queue=os.getenv("RABBITMQ_NUVOLO_VERIFICATION_QUEUE"),
                                    on_message_callback=self.__verification_callback)
        self._channel.basic_consume(queue=os.getenv("RABBITMQ_NUVOLO_PASS_RESET_QUEUE"),
                                    on_message_callback=self.__password_reset_callback)
        self._channel.basic_consume(queue=os.getenv("RABBITMQ_NUVOLO_NOTIFICATION_QUEUE"),
                                    on_message_callback=self.__notification_callback)
        self.logger.info("Starting RabbitMQ listener consuming.")
        self._channel.start_consuming()

    def __verification_callback(self, ch, method, properties, body):
        verification = json.loads(body)
        try:
            self.logger.info("Calling email service for verification email sending.")
            self._email_service.send_verification_email(verification)
            self.logger.info("Successfully sent verification email.")
            verification['success'] = 'true'
            self.__send_acknowledged_message(ch, method, properties, verification)
        except Exception as ex:
            verification['success'] = 'false'
            self.logger.error("Error occurred while sending verification email. {}", ex)
            self.__send_acknowledged_message(ch, method, properties, verification)

    def __password_reset_callback(self, ch, method, properties, body):
        pass_reset_request = json.loads(body)
        try:
            self.logger.info("Calling email service for verification email sending.")
            EmailService.send_pass_reset_email(pass_reset_request)
            self.logger.info("Successfully sent password reset request email.")
            pass_reset_request['success'] = 'true'
            self.__send_acknowledged_message(ch, method, properties, pass_reset_request)
        except Exception as ex:
            pass_reset_request['success'] = 'false'
            self.logger.error("Error occurred while sending password reset request. {}", ex)
            self.__send_acknowledged_message(ch, method, properties, pass_reset_request)

    def __notification_callback(self, ch, method, properties, body):
        notification = json.loads(body)
        try:
            EmailService.send_notification_email(notification)
            self.logger.info("Successfully sent notification email.")
            notification['success'] = 'true'
            self.__send_acknowledged_message(ch, method, properties, notification)
        except Exception as ex:
            notification['success'] = 'false'
            self.logger.error("Error occurred while sending notification email. {}", ex)
            self.__send_acknowledged_message(ch, method, properties, notification)

    def __send_acknowledged_message(self, ch, method, properties, message):
        self._channel.basic_publish(
            exchange='',
            routing_key=properties.reply_to,
            properties=pika.BasicProperties(correlation_id=properties.correlation_id),
            body=json.dumps(message).encode('utf-8'))
        ch.basic_ack(delivery_tag=method.delivery_tag)
        self.logger.info("Successfully acknowledged message")
