from django.db import models

# Create your models here.
class Stats(models.Model):
  robot_id = models.CharField(max_length=25)
  destiny = models.TextField()
  minutes = models.IntegerField(default=0)
  seconds = models.IntegerField(default=0)
  miliseconds = models.IntegerField(default=0)
