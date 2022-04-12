from django.contrib import admin
from .models import Route

# Register your models here.
class RouteAdmin(admin.ModelAdmin):
    list_display = ('origin_room', 'dest_room', 'route', 'return_route')

admin.site.register(Route, RouteAdmin)