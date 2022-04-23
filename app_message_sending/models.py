from django.db import models
from uuid import uuid4
from phone_field import PhoneField
from django.utils import timezone

# Create your models here.
"""
Сущность "рассылка" имеет атрибуты:
•
уникальный id рассылки
•
дата и время запуска рассылки
•
текст сообщения для доставки клиенту
•
фильтр свойств клиентов, на которых должна быть произведена рассылка (код мобильного оператора, тег)
•
дата и время окончания рассылки: если по каким-то причинам не успели разослать все сообщения - никакие сообщения клиентам после этого времени доставляться не должны

"""


class Client(models.Model):

    import pytz
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

    uid = models.UUIDField(primary_key=True, default=uuid4)
    phone_number = PhoneField(blank=True, help_text='Contact phone number', )
    operator_code = models.PositiveIntegerField(null=True)
    teg = models.CharField(max_length=100)
    timezone = models.CharField(max_length=32, choices=TIMEZONES, default='UTC')


class Mailing(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid4)
    date_created = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=500)
    filter_teg = models.CharField(max_length=50, blank=True)
    date_off = models.DateTimeField()

    @property
    def to_send(self):
        now = timezone.now()
        if self.beginning <= now <= self.ending:
            return True
        else:
            return False

    @property
    def sent_messages(self):
        return len(self.messages.filter(status='sent'))

    @property
    def messages_to_send(self):
        return len(self.messages.filter(status='proceeded'))

    @property
    def unsent_messages(self):
        return len(self.messages.filter(status='failed'))


class Message(models.Model):
    STATUS = (
        ('SEND', 'send'),
        ('PROCEEDED', 'proceeded'),
        ('FAILED', 'failed'),
    )

    uid = models.UUIDField(primary_key=True, default=uuid4)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=32, choices=STATUS)
    mailing_uid = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    client_uid = models.ForeignKey(Client, on_delete=models.CASCADE)


