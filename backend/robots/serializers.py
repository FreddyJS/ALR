from rest_framework import serializers

from .models import Robot
from routes.serializers import RouteSerializer


class RobotSerializer(serializers.ModelSerializer):
    route = RouteSerializer(read_only=True)

    class Meta:
        model = Robot
        fields = ['robot_id', 'robot_channel', 'ui_channel', 'hall', 'route' ,'active']
