from rest_framework import serializers
from .models import Stats


class StatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stats
        fields = ['robot_id', 'destiny', 'minutes', 'seconds', 'miliseconds']
