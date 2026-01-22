# django
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

# drf
from rest_framework.request import Request

User = get_user_model()


class EmailAuthenticationBackend(ModelBackend):
    """
    Custom authentication backend based on email instead of username
    """

    def authenticate(
        self,
        request: Request,
        username: str = None,
        password: str = None,
        **kwargs
    ):
        try:
            # Check if user with provided credentials are valid
            user = User.objects.get(email=username)
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id: int):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
