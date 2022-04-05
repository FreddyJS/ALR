# Create your views here.
from django.http import HttpRequest
from rest_framework import viewsets


from .models import Route
from .dijkstra import route_to_room
from .serializers import RouteSerializer


class RoutesViewSet(viewsets.ModelViewSet):
    lookup_field = 'dest_room'
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

    def retrieve(self, request: HttpRequest, *args, **kwargs):
        origin_room = request.GET.get('origin', "hall")
        degrees = int(request.GET.get('degrees', 0))
        dest_room = kwargs['dest_room']

        recalculate = True
        exists = Route.objects.filter(origin_room=origin_room, dest_room=dest_room).exists()
        if not exists or recalculate:
            try:
                if exists:
                    Route.objects.filter(origin_room=origin_room, dest_room=dest_room).delete()

                # Save the route to the database
                route = route_to_room(origin_room, dest_room, degrees)
                Route.objects.create(origin_room=origin_room, dest_room=dest_room, route=route)
            except ValueError:
                pass

        self.queryset = Route.objects.filter(origin_room=origin_room, dest_room=dest_room)
        return super().retrieve(request, *args, **kwargs)
