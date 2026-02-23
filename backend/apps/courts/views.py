"""
Vues pour la gestion des terrains.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from apps.courts.models import Court, Equipment, BlockedPeriod
from apps.courts.serializers import (
    CourtSerializer,
    CourtDetailSerializer,
    CourtListSerializer,
    EquipmentSerializer,
    BlockedPeriodSerializer,
    BlockedPeriodCreateSerializer
)
from apps.core.permissions import IsManager, IsAdmin, IsSiteManager


class EquipmentViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet pour les équipements."""
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [AllowAny]


class CourtViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des terrains."""
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['sport_type', 'site', 'is_active']
    search_fields = ['name', 'description', 'site__name']
    ordering_fields = ['name', 'price_per_hour', 'created_at']
    ordering = ['name']
    
    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Court.objects.filter(is_active=True)
        elif user.role.name == 'CLIENT':
            return Court.objects.filter(is_active=True)
        elif user.role.name == 'MANAGER':
            return Court.objects.filter(site__manager=user)
        return Court.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CourtListSerializer
        elif self.action == 'retrieve':
            return CourtDetailSerializer
        else:
            return CourtSerializer
    
    def get_permissions(self):
        if self.action in ['create']:
            return [IsAuthenticated(), IsManager() | IsAdmin()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return [AllowAny()]
    
    def perform_create(self, serializer):
        serializer.save()
    
    @action(detail=True, methods=['get'])
    def availability(self, request, pk=None):
        """Vérifier la disponibilité d'un terrain."""
        court = self.get_object()
        start = request.query_params.get('start')
        end = request.query_params.get('end')
        
        if not start or not end:
            return Response(
                {'error': 'start et end requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        from django.utils.dateparse import parse_datetime
        from apps.reservations.models import Reservation
        
        start_dt = parse_datetime(start)
        end_dt = parse_datetime(end)
        
        # Vérifier les réservations qui se chevauchent
        overlapping = Reservation.objects.filter(
            court=court,
            status__in=['CONFIRMED', 'PENDING'],
            start_datetime__lt=end_dt,
            end_datetime__gt=start_dt
        ).exists()
        
        # Vérifier les périodes bloquées
        blocked = court.blocked_periods.filter(
            start_datetime__lt=end_dt,
            end_datetime__gt=start_dt
        ).exists()
        
        is_available = not (overlapping or blocked)
        
        return Response({
            'court_id': court.id,
            'is_available': is_available,
            'start': start,
            'end': end
        })


class BlockedPeriodViewSet(viewsets.ModelViewSet):
    """ViewSet pour les périodes bloquées."""
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['court', 'court__site__manager']
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role.name == 'MANAGER':
            return BlockedPeriod.objects.filter(court__site__manager=user)
        elif user.role.name == 'ADMIN':
            return BlockedPeriod.objects.all()
        return BlockedPeriod.objects.none()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return BlockedPeriodCreateSerializer
        return BlockedPeriodSerializer
    
    @action(detail=False, methods=['post'])
    def create_multiple(self, request):
        """Créer plusieurs périodes bloquées à la fois."""
        periods = request.data
        created = []
        
        for period_data in periods:
            serializer = BlockedPeriodCreateSerializer(data=period_data)
            if serializer.is_valid():
                created.append(serializer.save())
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(
            BlockedPeriodSerializer(created, many=True).data,
            status=status.HTTP_201_CREATED
        )
