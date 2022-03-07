# Create your views here.
from rest_framework import viewsets

from .models import Route
from .serializers import RouteSerializer

# ViewSets define the view behavior.
class RoutesViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
