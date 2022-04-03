# Create your views here.
from rest_framework import viewsets


from .models import Route
from .dijkstra import get_final_route
from .serializers import RouteSerializer


class RoutesViewSet(viewsets.ModelViewSet):
    lookup_field = 'room'
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

    def retrieve(self, request, *args, **kwargs):
        room = kwargs['room']
        if not Route.objects.filter(room=room).exists():
            try:
                route = get_final_route("0", room)

                # Save the route to the database
                Route.objects.create(room=room, route=route)
            except ValueError:
                pass

        return super().retrieve(request, *args, **kwargs)
