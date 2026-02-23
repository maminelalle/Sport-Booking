"""
Sérialiseurs pour la gestion des terrains.
"""

from rest_framework import serializers
from apps.courts.models import Court, Equipment, CourtImage, BlockedPeriod
from apps.sites.models import Site


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ['id', 'name', 'description', 'icon']


class CourtImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourtImage
        fields = ['id', 'image', 'title', 'is_primary', 'uploaded_at']


class CourtSerializer(serializers.ModelSerializer):
    sport_type_name = serializers.CharField(source='get_sport_type_display', read_only=True)
    equipments = EquipmentSerializer(many=True, read_only=True)
    images = CourtImageSerializer(many=True, read_only=True)
    site_name = serializers.CharField(source='site.name', read_only=True)
    
    class Meta:
        model = Court
        fields = [
            'id', 'name', 'description', 'sport_type', 'sport_type_name',
            'site', 'site_name', 'price_per_hour', 'equipments', 'is_active',
            'capacity', 'images', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class CourtDetailSerializer(serializers.ModelSerializer):
    sport_type_name = serializers.CharField(source='get_sport_type_display', read_only=True)
    equipments = EquipmentSerializer(many=True, read_only=True)
    images = CourtImageSerializer(many=True, read_only=True)
    site = serializers.SerializerMethodField()
    
    class Meta:
        model = Court
        fields = [
            'id', 'name', 'description', 'sport_type', 'sport_type_name',
            'site', 'price_per_hour', 'equipments', 'is_active', 'capacity',
            'images', 'created_at'
        ]
    
    def get_site(self, obj):
        from apps.sites.serializers import SiteListSerializer
        return SiteListSerializer(obj.site).data


class CourtListSerializer(serializers.ModelSerializer):
    sport_type_name = serializers.CharField(source='get_sport_type_display', read_only=True)
    site_name = serializers.CharField(source='site.name', read_only=True)
    main_image = serializers.SerializerMethodField()
    
    class Meta:
        model = Court
        fields = [
            'id', 'name', 'sport_type', 'sport_type_name', 'site_name',
            'price_per_hour', 'capacity', 'main_image'
        ]
    
    def get_main_image(self, obj):
        image = obj.images.filter(is_primary=True).first()
        if not image:
            image = obj.images.first()
        return CourtImageSerializer(image).data if image else None


class BlockedPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlockedPeriod
        fields = ['id', 'court', 'start_datetime', 'end_datetime', 'reason', 'created_at']


class BlockedPeriodCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlockedPeriod
        fields = ['court', 'start_datetime', 'end_datetime', 'reason']
