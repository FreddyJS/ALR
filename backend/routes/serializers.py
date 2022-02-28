from rest_framework import serializers
from .models import Route


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['room']
    
    def to_representation(self, instance):
        rep =  super().to_representation(instance)
        rep['route'] = []

        steps = instance.route.split(';')
        for step in steps:
            rep['route'].append(step)

        return rep
