from rest_framework import viewsets
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework.decorators import action


from .models import Stats
from .serializers import StatsSerializer
from routes.models import Route

class StatsViewSet(viewsets.ModelViewSet):
    lookup_field = 'robot_id'
    queryset = Stats.objects.all()
    serializer_class = StatsSerializer

    def list(self, request, *args, **kwargs):
        # Example of how to use the channel layer in a viewset

        return super().list(request, *args, **kwargs)