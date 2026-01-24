# django
from django.contrib.auth import get_user_model

# drf
from rest_framework.viewsets import ViewSet, GenericViewSet, mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.request import Request

# local
from apps.authentication.services import UserService, AuthenticationService
from apps.authentication.serializers import (
    PerformTransactionSerializer,
    UserSerializer,
    CustomTokenObtainSerializer,
)

User = get_user_model()


# Create your views here.
class AuthenticationViewSet(ViewSet):
    serializer_class = CustomTokenObtainSerializer

    @action(detail=False, methods=["get"])
    def authentication_status(self, request: Request):
        """
        Check if user is authenticated to handle page state.
        Thanks to default authentication class, if user is not authenticated,
            HTTP_401 is returned automatically
        """
        return Response({"status": "authenticated"}, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[AllowAny],
        authentication_classes=[],
    )
    def login(self, request: Request):
        # Call login service. If tokens are missing, return HTTP_401
        data, msg = AuthenticationService.login(request)
        if not data:
            return Response({"status": msg}, status=status.HTTP_401_UNAUTHORIZED)

        # Set cookies and return HTTP_200 response
        response = Response({"status": msg}, status=status.HTTP_200_OK)
        AuthenticationService.set_refresh_token_cookie(response, data["refresh"])
        AuthenticationService.set_access_token_cookie(response, data["access"])
        return response

    @action(detail=False, methods=["post"], serializer_class=None)
    def logout(self, request: Request):
        AuthenticationService.logout(request)
        response = Response({"status": "logout successful"})
        AuthenticationService.clear_auth_cookies(response)
        return response

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[AllowAny],
        authentication_classes=[],
        url_path="token/refresh",
        serializer_class=None,
    )
    def refresh_token(self, request: Request):
        try:
            # Try to update token, if token missing, return HTTP_401
            # If refresh action failed, return HTTP_401 and clear cookies
            data, msg = AuthenticationService.refresh_token(request)
            if not data:
                return Response({"status": msg}, status=status.HTTP_401_UNAUTHORIZED)

            # Refresh token and set new values into cookies
            response = Response({"status": msg}, status=status.HTTP_200_OK)
            AuthenticationService.set_refresh_token_cookie(response, data["refresh"])
            AuthenticationService.set_access_token_cookie(response, data["access"])
            return response
        except TokenError as e:
            response = Response(
                {"status": "Invalid or expired token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
            AuthenticationService.clear_auth_cookies(response)
            return response


class UserViewSet(mixins.RetrieveModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action in ["deposit", "withdraw"]:
            return PerformTransactionSerializer
        return UserSerializer

    def _get_validated_amount(self, request: Request):
        """
        Helper method which reads amount.
        Created to avoid redundant code in "withdraw" and "deposit" endpoints
        """
        # Validate data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get data and proceed deposit
        return serializer.validated_data["amount"]

    @action(detail=True, methods=["post"])
    def deposit(self, request: Request, pk=None):
        amount = self._get_validated_amount(request)
        success, msg = UserService.deposit(pk, amount)

        if success:
            return Response({"msg": msg}, status=status.HTTP_200_OK)
        return Response({"msg": msg}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"])
    def withdraw(self, request: Request, pk=None):
        amount = self._get_validated_amount(request)
        success, msg = UserService.withdraw(pk, amount)

        if success:
            return Response({"msg": msg}, status=status.HTTP_200_OK)
        return Response({"msg": msg}, status=status.HTTP_400_BAD_REQUEST)
