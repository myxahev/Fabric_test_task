# import requests
# import os
# import time
# from dotenv import load_dotenv
# from .models import Mailing, Client, Message
#
# load_dotenv()
#
# URL = os.getenv("URL")
# TOKEN = os.getenv("TOKEN")
#
#
# def send_message(ids,
#                  url=URL,
#                  token=TOKEN):
#     """
#         отправка сообщения клиентам
#         через внешний АПИ сервис c JWT-авторизацией
#         адрес:
#         https://probe.fbrq.cloud/v1/send/{msgId}
#         содержание BODY:
#         {
#           "id": 0,
#           "phone": 0,
#           "text": "string"
#         }
#     """
#
#     header = {
#         'Authorization': f'Bearer {token}',
#         'Content-Type': 'application/json'}
#
#     mailing = Mailing.objects.filter(id=ids).first()
#     clients = Client.objects.filter(code=mailing.operator_code).all()
#
#     for client in clients:
#         messages = Message.objects.filter(client_id=client.id).select_related('client', 'mailing').all()
#
#         for message in messages:
#             data = {
#                 'id': message.uid,
#                 "phone": client.phone_number,
#                 "text": mailing.text
#             }
#             count = 0
#             try:
#                 response = requests.post(url=url + str(message.uid), headers=header, json=data)
#                 print(response.status_code)
#                 while response.status_code != 200 and count < 200:
#                     time.sleep(2)
#                     count += 1
#             except ConnectionError:
#                 return f'Connection error, contact your network administrator'

#
# from django.conf import settings
# from django.core.mail import send_mail
# from django.template import Engine, Context
# from Fabric_test_task.celery import app
#
#
# def render_template(template, context):
#     engine = Engine.get_default()
#     tmpl = engine.get_template(template)
#     return tmpl.render(Context(context))
#
#
# @celery_app.task(bind=True, default_retry_delay=10 * 60)
# def send_mail_task(self, recipients, subject, template, context):
#     message = render_template(f'{template}.txt', context)
#     html_message = render_template(f'{template}.html', context)
#     try:
#         send_mail(
#             subject=subject,
#             message=message,
#             from_email=settings.DEFAULT_FROM_EMAIL,
#             recipient_list=recipients,
#             fail_silently=False,
#             html_message=html_message
#         )
#     except smtplib.SMTPException as ex:
#         self.retry(exc=ex)

from django.core.mail import send_mail
from Fabric_test_task.celery import app
from .models import Client


@app.task
def send_beat_email():
    for client in Client.objects.all():
        send_mail(
            'Вы подписались на рассылку',
            'Мы будем присылать вам много спама каждые 10минут',
            'django.selery.test@gmail.com',
            'myxahev2@gmail.com',
            fail_silently=False,
        )