# django
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.conf import settings

# drf
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.response import Response
from rest_framework.request import Request

User = get_user_model()


class AuthenticationService:
    """
    Service which handles all logic related to authentication:
    login, logout, refreshing jwt token, setting and deleting
    jwt tokens from cookies
    """

    @staticmethod
    def login(request: Request):
        # Read credentials from request (payload)
        data = request.data
        email = data["email"]
        password = data["password"]

        # Validate user
        user = authenticate(request, username=email, password=password)
        if not user or not user.is_active:
            return None, "Invalid credentials"

        # Generate token
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, "logged in successfully"

    @staticmethod
    def logout(request: Request):
        # Read refresh token from cookie
        refresh_token = request.COOKIES.get("refresh_token")

        # Add token to black list
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except TokenError:
                pass

    @staticmethod
    def refresh_token(request: Request):
        # Read refresh token from cookie, if not return None with descriptive message
        refresh_token = request.COOKIES.get("refresh_token")

        if refresh_token is None:
            return None, "token not found"

        # Check user from token to ensure user is logged in.
        # Otherwise there's a big chance to enter in infinite validation flow.
        refresh = RefreshToken(refresh_token)
        if not refresh.payload.get("user_id"):
            raise TokenError("Token contains no user_id")

        # Refresh token
        refresh = RefreshToken(refresh_token)
        access = refresh.access_token
        return {
            "refresh": str(refresh),
            "access": str(access),
        }, "token refreshed successfully"

    @staticmethod
    def set_access_token_cookie(response: Response, access_token: str):
        # Set access token into cookies
        response.set_cookie(
            key="access_token",
            value=access_token,
            expires=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
            httponly=True,
            secure=False,
            path="/api/",
        )

    @staticmethod
    def set_refresh_token_cookie(response: Response, refresh_token: str):
        # Set refresh token into cookies
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            expires=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"],
            httponly=True,
            secure=False,
            path="/api/",
        )

    @staticmethod
    def clear_auth_cookies(response: Response):
        # Remove jwt tokens from cookies
        response.delete_cookie("access_token", "/api/")
        response.delete_cookie("refresh_token", "/api/")


class UserService:
    """
    Service to handle logic of user's actions
    """

    @staticmethod
    def withdraw(user_id: int, amount: float):
        # Validate input amount
        if amount < 1:
            return False, "Invalid amount value"

        # Validate user
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return False, "User does not exist"

        # Check if user has enough money on balance
        if amount > user.balance:
            return False, "Not enough money on user's balance"

        # Perform withdraw
        user.balance -= amount
        user.save()
        return True, f"Withdraw completed successfully. {amount=}"

    @staticmethod
    def deposit(user_id: int, amount: float):
        # Validate input amount
        if amount < 1:
            return False, "Invalid amount value"

        # Validate user
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return False, "User does not exist"
        except Exception as e:
            print(e)
            return False, "Something went wrong"

        # Perform deposit
        user.balance += amount
        user.save()
        return True, f"Deposit completed successfully. {amount=}"
