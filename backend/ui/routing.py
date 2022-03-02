from django.urls import re_path

from .consumers import UIConsumer

websocket_urlpatterns = [
    re_path(r'ws/ui/', UIConsumer.as_asgi()),
]