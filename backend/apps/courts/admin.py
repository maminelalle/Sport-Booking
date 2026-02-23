from django.contrib import admin
from .models import Court, CourtImage, Equipment, BlockedPeriod

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

class CourtImageInline(admin.TabularInline):
    model = CourtImage
    extra = 1
    fields = ['image', 'title', 'is_primary', 'uploaded_at']
    readonly_fields = ['uploaded_at']

@admin.register(Court)
class CourtAdmin(admin.ModelAdmin):
    list_display = ['name', 'site', 'sport_type', 'price_per_hour', 'is_active']
    list_filter = ['sport_type', 'site', 'is_active']
    search_fields = ['name', 'site__name']
    filter_horizontal = ['equipments']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [CourtImageInline]

@admin.register(CourtImage)
class CourtImageAdmin(admin.ModelAdmin):
    list_display = ['court', 'is_primary', 'uploaded_at']
    list_filter = ['is_primary', 'uploaded_at']
    search_fields = ['court__name']

@admin.register(BlockedPeriod)
class BlockedPeriodAdmin(admin.ModelAdmin):
    list_display = ['court', 'start_datetime', 'end_datetime', 'reason']
    list_filter = ['court', 'start_datetime']
    search_fields = ['court__name', 'reason']
