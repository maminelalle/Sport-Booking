"""
Serializers personnalisés pour JWT tokens.
"""

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Serializer personnalisé qui garantit user_id comme integer."""
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # S'assurer que user_id est un integer, pas un string
        token['user_id'] = int(user.id)
        return token


def get_tokens_for_user(user):
    """Générer des tokens JWT pour un utilisateur."""
    refresh = RefreshToken.for_user(user)
    # Forcer user_id comme integer
    refresh['user_id'] = int(user.id)
    refresh.access_token['user_id'] = int(user.id)
    
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
