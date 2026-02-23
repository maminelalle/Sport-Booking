"""
Vues pour la gestion des sites.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from apps.sites.models import Site, OpeningHours
from apps.sites.serializers import (
    SiteSerializer,
    SiteCreateUpdateSerializer,
    SiteListSerializer,
    OpeningHoursSerializer
)
from apps.core.permissions import IsManager, IsAdmin, IsSiteManager


class SiteViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des sites."""
    
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['city', 'is_active']
    search_fields = ['name', 'city', 'address']
    ordering_fields = ['name', 'created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        user = self.request.user
        if user.role.name == 'CLIENT':
            return Site.objects.filter(is_active=True)
        elif user.role.name == 'MANAGER':
            return Site.objects.filter(manager=user)
        return Site.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return SiteListSerializer
        elif self.action == 'create' or self.action == 'update':
            return SiteCreateUpdateSerializer
        return SiteSerializer
    
    def get_permissions(self):
        if self.action in ['create']:
            return [IsAuthenticated(), IsManager() | IsAdmin()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsSiteManager()]
        return super().get_permissions()
    
    @action(detail=True, methods=['get'])
    def opening_hours(self, request, pk=None):
        """Récupérer les horaires d'ouverture d'un site."""
        site = self.get_object()
        hours = site.opening_hours.all()
        serializer = OpeningHoursSerializer(hours, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def set_opening_hours(self, request, pk=None):
        """Définir les horaires d'ouverture."""
        site = self.get_object()
        self.check_object_permissions(request, site)
        
        for hour_data in request.data:
            OpeningHours.objects.update_or_create(
                site=site,
                day_of_week=hour_data['day_of_week'],
                defaults={
                    'open_time': hour_data['open_time'],
                    'close_time': hour_data['close_time']
                }
            )
        
        hours = site.opening_hours.all()
        serializer = OpeningHoursSerializer(hours, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OpeningHoursViewSet(viewsets.ModelViewSet):
    """ViewSet pour les horaires d'ouverture."""
    queryset = OpeningHours.objects.all()
    serializer_class = OpeningHoursSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role.name == 'CLIENT':
            return OpeningHours.objects.filter(site__is_active=True)
        elif user.role.name == 'MANAGER':
            return OpeningHours.objects.filter(site__manager=user)
        return OpeningHours.objects.all()
