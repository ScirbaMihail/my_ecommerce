# django
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.conf import settings

# drf
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

User = get_user_model()


class AuthenticationService:

    @staticmethod
    def login(request):
        data = request.data
        email = data["email"]
        password = data["password"]

        user = authenticate(request, username=email, password=password)

        if not user or not user.is_active:
            return None, "Invalid credentials"

        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, "logged in successfully"

    @staticmethod
    def logout(request):
        refresh_token = request.COOKIES.get("refresh_token")

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except TokenError:
                pass

    @staticmethod
    def refresh_token(request):
        refresh_token = request.COOKIES.get("refresh_token")

        if refresh_token is None:
            None, "token not found"

        refresh = RefreshToken(refresh_token)
        if not refresh.payload.get("user_id"):
            raise TokenError("Token contains no user_id")

        refresh = RefreshToken(refresh_token)
        access = refresh.access_token
        return {
            "refresh": str(refresh),
            "access": str(access),
        }, "token refreshed successfully"

    @staticmethod
    def set_access_token_cookie(response, access_token):
        response.set_cookie(
            key="access_token",
            value=access_token,
            expires=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
            httponly=True,
            secure=False,
            path="/api/auth/",
        )

    @staticmethod
    def set_refresh_token_cookie(response, refresh_token):
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            expires=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"],
            httponly=True,
            secure=False,
            path="/api/auth/",
        )

    @staticmethod
    def delete_jwt_token_cookies(response):
        response.delete_cookie("access_token", "/api/auth/")
        response.delete_cookie("refresh_token", "/api/auth/")


class UserService:

    @staticmethod
    def withdraw(user_id, amount):
        if amount < 1:
            return False, "Invalid amount value"

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return False, "User does not exist"

        if amount > user.balance:
            return False, "Not enough money on user's balance"

        user.balance -= amount
        user.save()
        return True, f"Withdraw completed successfully. {amount=}"

    @staticmethod
    def deposit(user_id, amount):
        if amount < 1:
            return False, "Invalid amount value"

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return False, "User does not exist"
        except Exception as e:
            print(e)
            return False, "Something went wrong"

        user.balance += amount
        user.save()
        return True, f"Deposit completed successfully. {amount=}"
