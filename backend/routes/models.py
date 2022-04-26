from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.
class Route(models.Model):
<<<<<<< HEAD
  origin_room = models.CharField(max_length=10)
  dest_room = models.CharField(max_length=10)
=======
  origin_room = models.TextField()
  dest_room = models.TextField()
>>>>>>> 4b36a36c1c2484eb6ac2b81b2f1f7bcd63327308
  route = ArrayField(models.TextField())
  return_route = ArrayField(models.TextField())

  class Meta:
    unique_together = [['origin_room', 'dest_room']]
