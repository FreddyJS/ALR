from django.urls import re_path

from .consumers import RobotConsumer

websocket_urlpatterns = [
    re_path(r'ws/(?P<connection_type>\w+)/(?P<robot_id>\w+)/', RobotConsumer.as_asgi()),
]