import time, json
from django.shortcuts import render
from channels.layers import get_channel_layer


async def home(request):
    for i in range(1, 11):
        channel_layer = get_channel_layer()
        data = {'count': i}

        await (channel_layer.group_send)(
            'new_consumer_group',
            {
                'type': 'send_notification',
                'value': json.dumps(data)
            }
        )
        time.sleep(2)
    return render(request, 'home.html')
