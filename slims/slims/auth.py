from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import get_user_model
import hashlib

class MD5AuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = get_user_model().objects.get(username=username)
        except get_user_model().DoesNotExist:
            return None

        # Check if the password is using MD5
        if len(user.password) == 32:  # MD5 hashes are 32 characters
            # If it matches the MD5 hash, authenticate and rehash password with Django’s default
            md5_hash = hashlib.md5(password.encode('utf-8')).hexdigest()
            if md5_hash == user.password:
                # Successfully authenticated with MD5 password, now rehash with Django's method
                user.password = make_password(password)
                user.save()
                return user
        # Default behavior for PBKDF2 or other Django hashers
        if check_password(password, user.password):
            return user

        return None
