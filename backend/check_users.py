import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sportsbooking.settings')
django.setup()

from apps.auth_app.models import CustomUser

users = CustomUser.objects.all()
print(f'Total users: {users.count()}\n')
for u in users:
    print(f'ID: {u.id}')
    print(f'Email: {u.email}')
    print(f'Username: {u.username}')
    print(f'Role: {u.role.name if u.role else None}')
    print('-' * 40)
