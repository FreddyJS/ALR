# Create your views here.
from django.contrib.auth.models import User
from rest_framework import viewsets

from routes.serializers import UserSerializer


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
