from rest_framework import serializers
from .models import Route


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['origin_room', 'dest_room', 'route', 'return_route']
