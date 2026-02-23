"""
Utilitaires pour l'API.
"""

from datetime import datetime, timedelta
from apps.courts.models import Court
from apps.reservations.models import Reservation


def get_court_availability(court: Court, start_date: datetime, end_date: datetime):
    """
    Récupérer la disponibilité d'un terrain pour une plage de dates.
    
    Retourne une liste des créneaux disponibles basée sur:
    - Les horaires d'ouverture du site
    - Les réservations existantes
    - Les périodes bloquées
    """
    
    # Récupérer les horaires d'ouverture du site
    site = court.site
    opening_hours = {h.day_of_week: h for h in site.opening_hours.all()}
    
    available_slots = []
    current = start_date
    
    while current < end_date:
        day_of_week = current.weekday()
        
        # Vérifier si le site est ouvert ce jour-là
        if day_of_week not in opening_hours:
            current += timedelta(days=1)
            current = current.replace(hour=0, minute=0, second=0)
            continue
        
        hours = opening_hours[day_of_week]
        slot_start = current.replace(
            hour=hours.open_time.hour,
            minute=hours.open_time.minute,
            second=0
        )
        slot_end = current.replace(
            hour=hours.close_time.hour,
            minute=hours.close_time.minute,
            second=0
        )
        
        # Vérifier les chevauchements avec les réservations
        overlapping_reservations = Reservation.objects.filter(
            court=court,
            status__in=['CONFIRMED', 'PENDING'],
            start_datetime__lt=slot_end,
            end_datetime__gt=slot_start
        ).order_by('start_datetime')
        
        # Vérifier les périodes bloquées
        blocked_periods = court.blocked_periods.filter(
            start_datetime__lt=slot_end,
            end_datetime__gt=slot_start
        ).order_by('start_datetime')
        
        # Construire les créneaux disponibles
        current_slot = max(slot_start, current)
        
        for reservation in overlapping_reservations:
            if current_slot < reservation.start_datetime:
                available_slots.append({
                    'start': current_slot,
                    'end': reservation.start_datetime
                })
            current_slot = reservation.end_datetime
        
        if current_slot < slot_end:
            available_slots.append({
                'start': current_slot,
                'end': slot_end
            })
        
        current += timedelta(days=1)
        current = current.replace(hour=0, minute=0, second=0)
    
    return available_slots
