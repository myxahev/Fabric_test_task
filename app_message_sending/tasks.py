import requests
import os
import time
from dotenv import load_dotenv
from .models import Mailing, Client, Message
from django.core.mail import send_mail
from .models import Client
from celery import shared_task
import smtplib
from django.conf import settings

load_dotenv()

URL = os.getenv("URL")
TOKEN = os.getenv("TOKEN")

@shared_task(name="send_message")
def send_message(ids,
                 url=URL,
                 token=TOKEN):
    """
        отправка сообщения клиентам
        через внешний АПИ сервис c JWT-авторизацией
        адрес:
        https://probe.fbrq.cloud/v1/send/{msgId}
        содержание BODY:
        {
          "id": 0,
          "phone": 0,
          "text": "string"
        }
    """

    header = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'}

    mailing = Mailing.objects.filter(id=ids).first()
    clients = Client.objects.filter(code=mailing.operator_code).all()

    for client in clients:
        messages = Message.objects.filter(client_id=client.id).select_related('client', 'mailing').all()

        for message in messages:
            data = {
                'id': message.uid,
                "phone": client.phone_number,
                "text": mailing.text
            }
            count = 0
            try:
                response = requests.post(url=url + str(message.uid), headers=header, json=data)
                print(response.status_code)
                while response.status_code != 200 and count < 200:
                    time.sleep(2)
                    count += 1
            except ConnectionError:
                return f'Connection error, contact your network administrator'


@shared_task(name="send_beat_email")
def send_beat_email():
    try:
        send_mail(
            subject='Вы подписались на рассылку логов',
            message='log',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=['myxahev2@gmail.com'],
            # fail_silently=False,
            html_message='здесь будет лог'
        )
    except smtplib.SMTPException as ex:
        send_beat_email.retry(exc=ex)
