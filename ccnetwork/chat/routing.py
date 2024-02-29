from django.template.defaulttags import url
from django.urls import path

from . import consumers


websocket_urlpatterns = [
    path('ws/<str:uuid>/', consumers.ChatConsumer.as_asgi()),
]