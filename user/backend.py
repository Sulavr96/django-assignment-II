from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

USER = get_user_model()


class EmailBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = USER.objects.get(email=username)
        except USER.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None

