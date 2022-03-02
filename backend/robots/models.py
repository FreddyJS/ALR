from django.db import models

# Create your models here.
class Robot(models.Model):
  robot_id = models.CharField(max_length=25, unique=True)
  robot_channel = models.TextField()
  ui_channel = models.TextField(null=True)
