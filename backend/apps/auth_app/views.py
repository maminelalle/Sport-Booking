"""
Vues pour l'authentification.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from apps.auth_app.models import CustomUser, Role
from apps.auth_app.serializers import (
    UserSerializer,
    UserCreateSerializer,
    LoginSerializer,
    RoleSerializer
)
from apps.auth_app.jwt_serializers import get_tokens_for_user


class RoleViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet pour les rôles."""
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [AllowAny]


class AuthViewSet(viewsets.ViewSet):
    """ViewSet pour l'authentification."""
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        """Créer un nouvel utilisateur."""
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'user': UserSerializer(user).data,
                'message': 'Utilisateur créé avec succès'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        """Connecter un utilisateur et générer les tokens JWT."""
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            tokens = get_tokens_for_user(user)
            
            return Response({
                'user': UserSerializer(user).data,
                'access': tokens['access'],
                'refresh': tokens['refresh'],
                'message': 'Connecté avec succès'
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def me(self, request):
        """Récupérer les informations de l'utilisateur connecté ou par email."""
        # Try to get from auth token first
        if request.user and request.user.is_authenticated:
            return Response(UserSerializer(request.user).data)
        
        # Fall back to email parameter
        user_email = request.query_params.get('user_email', None)
        if user_email:
            try:
                user = CustomUser.objects.get(email=user_email)
                return Response(UserSerializer(user).data)
            except CustomUser.DoesNotExist:
                return Response(
                    {'error': 'Utilisateur non trouvé'},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        return Response(
            {'error': 'Non authentifié et pas d\'email fourni'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        """Déconnecter l'utilisateur."""
        try:
            refresh = request.data.get('refresh')
            token = RefreshToken(refresh)
            token.blacklist()
            return Response(
                {'message': 'Déconnecté avec succès'},
                status=status.HTTP_200_OK
            )
        except Exception:
            return Response(
                {'error': 'Token invalide'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def refresh_token(self, request):
        """Rafraîchir le token d'accès."""
        try:
            refresh = RefreshToken(request.data.get('refresh'))
            return Response({
                'access': str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {'error': 'Token invalide'},
                status=status.HTTP_400_BAD_REQUEST
            )


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des utilisateurs."""
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Un client ne voit que son propre profil
        user = self.request.user
        if user.role.name == 'CLIENT':
            return CustomUser.objects.filter(id=user.id)
        # Les managers et admin voient tous les utilisateurs
        return CustomUser.objects.all()
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def profile(self, request):
        """Récupérer le profil de l'utilisateur connecté."""
        return Response(UserSerializer(request.user).data)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def profile_update(self, request):
        """Mettre à jour le profil de l'utilisateur connecté."""
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        """Changer le mot de passe de l'utilisateur."""
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        
        if not user.check_password(old_password):
            return Response(
                {'error': 'Ancien mot de passe incorrect'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.set_password(new_password)
        user.save()
        
        return Response({'message': 'Mot de passe modifié avec succès'})
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def delete_account(self, request):
        """Supprimer le compte de l'utilisateur (RGPD)."""
        user = request.user
        password = request.data.get('password')
        
        if not user.check_password(password):
            return Response(
                {'error': 'Mot de passe incorrect'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.delete()
        return Response({'message': 'Compte supprimé avec succès'})
