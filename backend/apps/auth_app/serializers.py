"""
Sérialiseurs pour l'authentification et gestion des utilisateurs.
"""

from rest_framework import serializers
from django.contrib.auth import authenticate
from apps.auth_app.models import CustomUser, Role


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'description']


class UserSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='role.name', read_only=True)
    
    class Meta:
        model = CustomUser
        fields = [
            'id', 'email', 'first_name', 'last_name', 'phone', 
            'role', 'role_name', 'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password_confirm = serializers.CharField(write_only=True, required=True)
    role = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(),
        required=False,
        allow_null=True
    )
    
    class Meta:
        model = CustomUser
        fields = [
            'email', 'first_name', 'last_name', 'phone', 'password', 
            'password_confirm', 'role', 'gdpr_consent'
        ]
    
    def validate(self, data):
        if data['password'] != data.pop('password_confirm'):
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas."})
        return data
    
    def create(self, validated_data):
        # Assign CLIENT role by default if not provided
        if 'role' not in validated_data or validated_data.get('role') is None:
            client_role = Role.objects.get(name='CLIENT')
            validated_data['role'] = client_role
        
        user = CustomUser.objects.create_user(
            username=validated_data['email'],  # Use email as username
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone=validated_data.get('phone', ''),
            password=validated_data['password'],
            role=validated_data.get('role'),
            gdpr_consent=validated_data.get('gdpr_consent', False)
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Email ou mot de passe incorrect.")
        data['user'] = user
        return data
