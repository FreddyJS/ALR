from rest_framework import viewsets
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework.decorators import action


from .models import Robot
from .serializers import RobotSerializer
from routes.models import Route

class RobotsViewSet(viewsets.ModelViewSet):
    lookup_field = 'robot_id'
    queryset = Robot.objects.all()
    serializer_class = RobotSerializer

    def list(self, request, *args, **kwargs):
        # Example of how to use the channel layer in a viewset
        try:
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
        except Exception:
            pass

        return super().list(request, *args, **kwargs)

    @action(detail=True, methods=['put'])
    def hall(self, request, *args, **kwargs):
        ''' Set the hall of the robot '''
        robot: Robot = self.get_object()
        robot.hall = request.data['hall']
        robot.save()

        # TODO: Update the UI with the new hall
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.send)(robot.ui_channel, {
                'type': 'to.ui',
                'hall': robot.hall
            })
        return self.retrieve(request, *args, **kwargs)

        

    @action(detail=True, methods=['put'])
    def active(self, request, *args, **kwargs):
        robot: Robot = self.get_object()
        robot.active = request.data['active']
        route = request.data['route']
        robot.route = Route.objects.filter(origin_room=route['origin_room'], dest_room=route['dest_room']).first()
        robot.save()

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.send)(robot.ui_channel, {
                'type': 'to.ui',
                'active': robot.active,
                'route': route
            })
        return self.retrieve(request, *args, **kwargs)
