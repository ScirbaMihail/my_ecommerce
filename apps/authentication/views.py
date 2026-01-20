# django
from django.contrib.auth import get_user_model
from django.conf import settings

# drf
from rest_framework.viewsets import ViewSet, GenericViewSet, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.exceptions import TokenError

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
    def authentication_status(self, request):
        return Response({"status": "authenticated"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def login(self, request):
        data, msg = AuthenticationService.login(request)
        if not data:
            return Response({"status": msg}, status=status.HTTP_401_UNAUTHORIZED)

        response = Response({"status": msg}, status=status.HTTP_200_OK)

        self._set_cookies(response, data["access"], data["refresh"])
        return response

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[AllowAny],
        url_path="token/refresh",
        serializer_class=None
    )
    def refresh_token(self, request):
        try:
            data, msg = AuthenticationService.refresh_token(request)
            if not data:
                return Response({"status": msg}, status=status.HTTP_401_UNAUTHORIZED)

            access, refresh = data["access"], data["refresh"]

            response = Response({"status": msg}, status=status.HTTP_200_OK)
            self._set_cookies(response, access, refresh)

            return response
        except TokenError as e:
            return Response(
                {"status": "Invalid or expired token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

    def _set_cookies(self, response: Response, access_token, refresh_token):
        jwt_settings = settings.SIMPLE_JWT
        response.set_cookie(
            key="access_token",
            value=access_token,
            expires=jwt_settings["ACCESS_TOKEN_LIFETIME"],
            httponly=True,
            secure=False,
            path="/api/auth/",
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            expires=jwt_settings["REFRESH_TOKEN_LIFETIME"],
            httponly=True,
            secure=False,
            path="/api/auth/",
        )


class UserViewSet(mixins.RetrieveModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action in ["deposit", "withdraw"]:
            return PerformTransactionSerializer
        return UserSerializer

    def _get_validated_amount(self, request):
        # Validate data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get data and proceed deposit
        return serializer.validated_data["amount"]

    @action(detail=True, methods=["post"])
    def deposit(self, request, pk=None):
        amount = self._get_validated_amount(request)
        success, msg = UserService.deposit(pk, amount)

        if success:
            return Response({"msg": msg}, status=status.HTTP_200_OK)
        return Response({"msg": msg}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"])
    def withdraw(self, request, pk=None):
        amount = self._get_validated_amount(request)
        success, msg = UserService.withdraw(pk, amount)

        if success:
            return Response({"msg": msg}, status=status.HTTP_200_OK)
        return Response({"msg": msg}, status=status.HTTP_400_BAD_REQUEST)
