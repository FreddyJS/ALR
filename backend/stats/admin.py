from django.contrib import admin
from .models import Stats
# Register your models here.


class AdminStats(admin.ModelAdmin):
    list_display = ['robot_id', 'destiny', 'minutes', 'seconds', 'miliseconds']

admin.site.register(Stats, AdminStats)