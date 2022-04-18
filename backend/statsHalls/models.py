from django.db import models

# Create your models here.
class StatsHalls(models.Model):
  hall = models.TextField()
  stopped = models.IntegerField(default=0)


