#!/usr/bin/env python
import os
import django
from django.conf import settings

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sportsbooking.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Set password for admin user
try:
    admin = User.objects.get(username='admin')
    admin.set_password('admin123456')
    admin.save()
    print('✅ Mot de passe défini avec succès!')
    print(f'   Nom d\'utilisateur: admin')
    print(f'   Mot de passe: admin123456')
    print(f'   Email: {admin.email}')
except User.DoesNotExist:
    print('❌ Utilisateur admin non trouvé')
except Exception as e:
    print(f'❌ Erreur: {str(e)}')
