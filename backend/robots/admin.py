from django.contrib import admin

from .models import Robot

class AdminRobot(admin.ModelAdmin):
    list_display = ['robot_id', 'robot_channel', 'ui_channel', 'hall', 'route' ,'active']

admin.site.register(Robot, AdminRobot)