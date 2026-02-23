from django.contrib import admin
from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'court', 'start_datetime', 'status', 'total_amount']
    list_filter = ['status', 'start_datetime', 'court__site']
    search_fields = ['user__email', 'court__name']
    readonly_fields = ['created_at', 'updated_at', 'cancelled_at', 'total_amount']
    fieldsets = (
        ('Informations de base', {
            'fields': ('user', 'court', 'status')
        }),
        ('Plage horaire', {
            'fields': ('start_datetime', 'end_datetime')
        }),
        ('Tarification', {
            'fields': ('price_per_hour', 'total_amount')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'cancelled_at'),
            'classes': ('collapse',)
        }),
    )
