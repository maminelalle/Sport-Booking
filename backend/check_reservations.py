#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sportsbooking.settings')
django.setup()

from apps.reservations.models import Reservation
from apps.courts.models import Court
from django.utils import timezone
from datetime import timedelta

# Show all reservations
print("=== EXISTING RESERVATIONS ===")
for res in Reservation.objects.all().order_by('start_datetime'):
    print(f"Court: {res.court.name}, User: {res.user.email}, Time: {res.start_datetime.strftime('%Y-%m-%d %H:%M')} to {res.end_datetime.strftime('%H:%M')}, Status: {res.status}")

# Show which courts are available
print("\n=== AVAILABLE TIME SLOTS ===")
now = timezone.now()
future = now + timedelta(days=7)

booked_courts = Reservation.objects.filter(
    start_datetime__lte=future,
    end_datetime__gte=now,
    status__in=['CONFIRMED', 'PENDING']
).values_list('court_id', flat=True).distinct()

available = Court.objects.exclude(id__in=booked_courts).filter(is_active=True)[:3]
for court in available:
    print(f"✓ {court.name} ({court.sport_type}) - Available for booking")
