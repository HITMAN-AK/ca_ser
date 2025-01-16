"""
ASGI config for ca_django project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path,re_path
from server.consumers import ChatConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE','ca_django.settings')


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            re_path(r'ws/chat/(?P<username>\w+)/(?P<other_user>\w+)/$',ChatConsumer.as_asgi()),
        ])
    ),
})