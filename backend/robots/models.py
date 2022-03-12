from django.db import models

from routes.models import Route

# Create your models here.
class Robot(models.Model):
  robot_id = models.CharField(max_length=25, unique=True)
  robot_channel = models.TextField()
  ui_channel = models.TextField(null=True)
  active = models.BooleanField(default=False)
  route = models.ForeignKey(Route, on_delete=models.SET_NULL, null=True)
  hall = models.IntegerField(default=0) # TODO: Change to a foreign key to a hall
