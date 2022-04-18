"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from rest_framework import routers
from django.urls import include, path
from routes import views as routes_views
from robots import views as robots_views
from stats import views as stats_views
from statsHalls import views as statsHalls_views

router = routers.DefaultRouter()
router.register('routes', routes_views.RoutesViewSet)
router.register('robots', robots_views.RobotsViewSet)
router.register('stats', stats_views.StatsViewSet)
router.register('statsHalls', statsHalls_views.StatsHallsViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
