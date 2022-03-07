from rest_framework import viewsets
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .models import Robot
from .serializers import RobotSerializer

class RobotsViewSet(viewsets.ModelViewSet):
    queryset = Robot.objects.all()
    serializer_class = RobotSerializer

    def list(self, request, *args, **kwargs):
        # Example of how to use the channel layer in a viewset
        first: Robot = self.queryset.first()
        channel_layer = get_channel_layer()

        # Send a message to the group
        async_to_sync(channel_layer.group_send)(first.robot_id, {
            'type': 'to.ui',
            'message': 'Hello from RobotsViewSet'
        })

        # Send a message to the robot, using the robot channel
        async_to_sync(channel_layer.send)(first.robot_channel, {
            'type': 'to.robot',
            'message': 'Hello from RobotsViewSet'
        })

        return super().list(request, *args, **kwargs)
