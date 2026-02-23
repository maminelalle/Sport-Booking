"""
URLs pour la gestion des terrains.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourtViewSet, EquipmentViewSet, BlockedPeriodViewSet

router = DefaultRouter()
router.register(r'courts', CourtViewSet, basename='court')
router.register(r'equipments', EquipmentViewSet, basename='equipment')
router.register(r'blocked-periods', BlockedPeriodViewSet, basename='blocked-period')

app_name = 'courts'

urlpatterns = [
    path('', include(router.urls)),
]
