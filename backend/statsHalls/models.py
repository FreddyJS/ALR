from django.db import models

# Create your models here.
class StatsHalls(models.Model):
  hall = models.TextField(unique=True)
  stopped = models.IntegerField(default=0)


