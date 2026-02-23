"""
URLs pour l'authentification.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthViewSet, UserViewSet, RoleViewSet

router = DefaultRouter()
router.register(r'roles', RoleViewSet, basename='role')
router.register(r'users', UserViewSet, basename='user')
router.register(r'', AuthViewSet, basename='auth')

app_name = 'auth'

urlpatterns = [
    path('', include(router.urls)),
]
