from django.shortcuts import render
from rest_framework import viewsets
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework.decorators import action


from .models import StatsHalls
from .serializers import StatsHallsSerializer
from routes.models import Route

class StatsHallsViewSet(viewsets.ModelViewSet):
    lookup_field = 'hall'
    queryset = StatsHalls.objects.all()
    serializer_class = StatsHallsSerializer

    def list(self, request, *args, **kwargs):
        # Example of how to use the channel layer in a viewset

        return super().list(request, *args, **kwargs)
