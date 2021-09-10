"""
ASGI config for django_channels project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path
from main import consumers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_channels.settings')

application = get_asgi_application()

ws_patterns = [
    path('ws/test/', consumers.TestConsumer.as_asgi()),
    path('ws/new/', consumers.NewConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    'websocket': URLRouter(ws_patterns)
})
