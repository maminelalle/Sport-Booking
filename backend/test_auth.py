import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sportsbooking.settings')
django.setup()

from django.contrib.auth import authenticate
from apps.auth_app.models import CustomUser

# Test with existing user
print("=== Testing Authentication ===")
user = CustomUser.objects.get(username='client1')
print(f"User found: {user.email}")
print(f"Username field: {user.username}")
print(f"Check password 'password123': {user.check_password('password123')}")
print(f"Check password 'client123456': {user.check_password('client123456')}")

# Try authenticate
auth_result = authenticate(email=user.email, password='client123456')
print(f"Authenticate with email: {auth_result}")

# Try with username
auth_result2 = authenticate(username=user.username, password='client123456')
print(f"Authenticate with username: {auth_result2}")

# Check USERNAME_FIELD
print(f"\nUSERNAME_FIELD: {CustomUser.USERNAME_FIELD}")
