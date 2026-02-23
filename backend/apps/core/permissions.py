"""
Permissions personnalisées pour l'API.
"""

from rest_framework import permissions


class IsClient(permissions.BasePermission):
    """Permettre l'accès aux utilisateurs avec le rôle CLIENT."""
    def has_permission(self, request, view):
        return request.user and request.user.role.name == 'CLIENT'


class IsManager(permissions.BasePermission):
    """Permettre l'accès aux utilisateurs avec le rôle MANAGER."""
    def has_permission(self, request, view):
        return request.user and request.user.role.name == 'MANAGER'


class IsAdmin(permissions.BasePermission):
    """Permettre l'accès aux utilisateurs avec le rôle ADMIN."""
    def has_permission(self, request, view):
        return request.user and request.user.role.name == 'ADMIN'


class IsSiteManager(permissions.BasePermission):
    """Vérifier que l'utilisateur gère le site en question."""
    def has_object_permission(self, request, view, obj):
        if request.user.role.name == 'ADMIN':
            return True
        return obj.manager == request.user


class IsOwnReservation(permissions.BasePermission):
    """Vérifier que l'utilisateur est le propriétaire de la réservation."""
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff
