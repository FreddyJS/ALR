from rest_framework import serializers
from .models import StatsHalls


class StatsHallsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatsHalls
        fields = ['hall', 'stopped']
