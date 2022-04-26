from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.
class Route(models.Model):
  origin_room = models.TextField()
  dest_room = models.TextField()
  route = ArrayField(models.TextField())
  return_route = ArrayField(models.TextField())

  class Meta:
    unique_together = [['origin_room', 'dest_room']]
