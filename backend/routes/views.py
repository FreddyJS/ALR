# Create your views here.
from rest_framework import viewsets

from .models import Route
from .serializers import RouteSerializer

# ViewSets define the view behavior.
class RoutesViewSet(viewsets.ModelViewSet):
    lookup_field = 'room'
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
