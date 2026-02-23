from django.contrib import admin
from .models import Site, OpeningHours, SiteImage

class SiteImageInline(admin.TabularInline):
    model = SiteImage
    extra = 1
    fields = ['image', 'title', 'description', 'is_primary', 'uploaded_at']
    readonly_fields = ['uploaded_at']

@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'manager', 'is_active', 'created_at']
    list_filter = ['city', 'is_active', 'created_at']
    search_fields = ['name', 'city', 'address']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [SiteImageInline]
    fieldsets = (
        ('Informations générales', {
            'fields': ('name', 'description', 'manager')
        }),
        ('Localisation', {
            'fields': ('address', 'city', 'postal_code', 'latitude', 'longitude')
        }),
        ('Statut', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(OpeningHours)
class OpeningHoursAdmin(admin.ModelAdmin):
    list_display = ['site', 'day_of_week', 'open_time', 'close_time']
    list_filter = ['day_of_week', 'site']
    search_fields = ['site__name']


@admin.register(SiteImage)
class SiteImageAdmin(admin.ModelAdmin):
    list_display = ['site', 'is_primary', 'title', 'uploaded_at']
    list_filter = ['is_primary', 'uploaded_at', 'site']
    search_fields = ['site__name', 'title']
    readonly_fields = ['uploaded_at']
