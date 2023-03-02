from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class PasswordlessAuthBackend(ModelBackend):
    """ Login to Django without providing a password. """

    def authenticate(self, request, phone_number):
        User = get_user_model()
        try:
            user = User.objects.get(phone_number=phone_number)
            return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None