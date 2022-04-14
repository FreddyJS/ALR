from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.
class Route(models.Model):
  origin_room = models.CharField(max_length=5)
  dest_room = models.CharField(max_length=5)
  route = ArrayField(models.TextField())
  return_route = ArrayField(models.TextField())

  class Meta:
    unique_together = [['origin_room', 'dest_room']]
