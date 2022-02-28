# Create your views here.
from rest_framework import viewsets

from .serializers import RouteSerializer
from .models import Route


# ViewSets define the view behavior.
class RoutesViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
