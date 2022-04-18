from django.contrib import admin
from .models import StatsHalls
# Register your models here.


class AdminStatsHalls(admin.ModelAdmin):
    list_display = ['hall', 'stopped']

admin.site.register(StatsHalls, AdminStatsHalls)