import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sportsbooking.settings')
django.setup()

from apps.auth_app.models import CustomUser

# Test 1: Lookup with string
try:
    user_string = CustomUser.objects.get(id="3")
    print(f"✅ Test 1: Lookup with string '3' SUCCESS")
    print(f"   Found: {user_string.email}")
except CustomUser.DoesNotExist:
    print("❌ Test 1: Lookup with string '3' FAILED - User not found")
except Exception as e:
    print(f"❌ Test 1: Lookup with string '3' ERROR: {e}")

# Test 2: Lookup with integer
try:
    user_int = CustomUser.objects.get(id=3)
    print(f"✅ Test 2: Lookup with integer 3 SUCCESS")
    print(f"   Found: {user_int.email}")
except CustomUser.DoesNotExist:
    print("❌ Test 2: Lookup with integer 3 FAILED - User not found")
except Exception as e:
    print(f"❌ Test 2: Lookup with integer 3 ERROR: {e}")

# Test 3: Check if user 3 exists
try:
    user = CustomUser.objects.filter(id=3).first()
    if user:
        print(f"\n✅ User ID 3 EXISTS in database")
        print(f"   ID type: {type(user.id)}")
        print(f"   Email: {user.email}")
        print(f"   Username: {user.username}")
        print(f"   USERNAME_FIELD: {CustomUser.USERNAME_FIELD}")
    else:
        print("\n❌ No user with ID 3 found")
except Exception as e:
    print(f"\n❌ Error checking user: {e}")
