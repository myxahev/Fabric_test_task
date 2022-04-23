import requests
import os
import time
from dotenv import load_dotenv
from .models import Mailing, Client, Message

load_dotenv()

URL = os.getenv("URL")
TOKEN = os.getenv("TOKEN")


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