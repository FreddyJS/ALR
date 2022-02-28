from django.contrib import admin
from .models import Route

# Register your models here.
class RouteAdmin(admin.ModelAdmin):
    list_display = ('room', 'route')

admin.site.register(Route, RouteAdmin)