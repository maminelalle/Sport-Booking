"""
Sérialiseurs pour la gestion des sites.
"""

from rest_framework import serializers
from apps.sites.models import Site, OpeningHours, SiteImage


class SiteImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteImage
        fields = ['id', 'image', 'title', 'description', 'is_primary', 'uploaded_at']


class OpeningHoursSerializer(serializers.ModelSerializer):
    day_name = serializers.CharField(source='get_day_of_week_display', read_only=True)
    
    class Meta:
        model = OpeningHours
        fields = ['id', 'site', 'day_of_week', 'day_name', 'open_time', 'close_time']


class SiteSerializer(serializers.ModelSerializer):
    manager_name = serializers.CharField(source='manager.get_full_name', read_only=True)
    opening_hours = OpeningHoursSerializer(many=True, read_only=True)
    images = SiteImageSerializer(many=True, read_only=True)
    courts_count = serializers.SerializerMethodField()
    primary_image = serializers.SerializerMethodField()
    
    class Meta:
        model = Site
        fields = [
            'id', 'name', 'description', 'address', 'city', 'postal_code',
            'latitude', 'longitude', 'manager', 'manager_name', 'is_active',
            'created_at', 'opening_hours', 'images', 'primary_image', 'courts_count'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_courts_count(self, obj):
        return obj.courts.filter(is_active=True).count()
    
    def get_primary_image(self, obj):
        primary = obj.images.filter(is_primary=True).first()
        return SiteImageSerializer(primary).data if primary else None


class SiteCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = [
            'name', 'description', 'address', 'city', 'postal_code',
            'latitude', 'longitude', 'manager', 'is_active'
        ]


class SiteListSerializer(serializers.ModelSerializer):
    manager_name = serializers.CharField(source='manager.get_full_name', read_only=True)
    primary_image = serializers.SerializerMethodField()
    courts_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Site
        fields = [
            'id', 'name', 'city', 'manager_name', 'is_active', 'courts_count', 'primary_image'
        ]
    
    def get_courts_count(self, obj):
        return obj.courts.filter(is_active=True).count()
    
    def get_primary_image(self, obj):
        primary = obj.images.filter(is_primary=True).first()
        return SiteImageSerializer(primary).data if primary else None
