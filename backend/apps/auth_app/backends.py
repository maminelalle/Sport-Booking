"""
Custom authentication backend for email-based authentication.
"""

from django.contrib.auth.backends import ModelBackend
from apps.auth_app.models import CustomUser


class EmailBackend(ModelBackend):
    """
    Authenticate using email address instead of username.
    """
    
    def authenticate(self, request, username=None, password=None, email=None, **kwargs):
        """
        Authenticate a user based on email address as the username.
        """
        # Allow both username and email parameters
        email_or_username = email or username
        
        if email_or_username is None or password is None:
            return None
        
        try:
            # Try to fetch the user by searching the email field
            user = CustomUser.objects.get(email=email_or_username)
        except CustomUser.DoesNotExist:
            # Run the default password hasher once to reduce timing difference
            CustomUser().set_password(password)
            return None
        
        # Check the password
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        
        return None
