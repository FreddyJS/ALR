from django.urls import re_path

from .consumers import StatsConsumer

websocket_urlpatterns = [
    re_path(r'ws/(?P<connection_type>\w+)/(?P<robot_id>\w+)/', StatsConsumer.as_asgi()),
]