from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError


class CookieJWTAuthentication(JWTAuthentication):
    """
    Custom authentication based on tokens stored in cookies instead of
    header authentication.
    """

    def authenticate(self, request):
        raw_token = request.COOKIES.get("access_token")

        if raw_token is None:
            return None

        try:
            validated_token = self.get_validated_token(raw_token)
            return self.get_user(validated_token), validated_token
        except TokenError as e:
            return None
