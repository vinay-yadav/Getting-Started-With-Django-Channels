import json
from django.db import models
from django.contrib.auth import get_user_model
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


User = get_user_model()


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification = models.CharField(max_length=100)
    is_seen = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} {self.notification} {"seen" if self.is_seen else "No"}'

    def save(self, *args, **kwargs):
        print(self)
        channel_layer = get_channel_layer()
        data = {
            'unreadMessageCount': Notification.objects.filter(is_seen=False).count(),
            'currentMsg': self.notification
        }

        async_to_sync(channel_layer.group_send)(
            'test_consumer_group',
            {
                'type': 'send_notification',
                'value': json.dumps(data)
            }
        )
        super(Notification, self).save(*args, **kwargs)

