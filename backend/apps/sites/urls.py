"""
URLs pour la gestion des sites.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SiteViewSet, OpeningHoursViewSet

router = DefaultRouter()
router.register(r'', SiteViewSet, basename='site')
router.register(r'opening-hours', OpeningHoursViewSet, basename='opening-hours')

app_name = 'sites'

urlpatterns = [
    path('', include(router.urls)),
]
