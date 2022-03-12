from rest_framework import serializers
from .models import Robot


class RobotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Robot
        fields = ['robot_id', 'robot_channel', 'ui_channel', 'hall', 'route' ,'active']
