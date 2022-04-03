from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.
class Route(models.Model):
  room = models.CharField(max_length=5, unique=True)
  route = ArrayField(models.TextField())
