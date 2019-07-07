from django.db import models
from django.db.models.signals import post_save
from model_utils.models import TimeStampedModel

from notification.pusher import send_push_notification


def notification_post_save(sender, instance, created, **kwargs):
    if created:
        send_push_notification(instance)


class Notification(TimeStampedModel):
    title = models.CharField(max_length=30, default='Hello Aidmate')
    message = models.CharField(max_length=100, default='push notification message test.', blank=True)

    def __str__(self):
        return f'{self.id}:{self.title}'


post_save.connect(receiver=notification_post_save, sender=Notification)
