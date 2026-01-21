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

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[AllowAny],
        authentication_classes=[],
    )
    def login(self, request):
        data, msg = AuthenticationService.login(request)
        if not data:
            return Response({"status": msg}, status=status.HTTP_401_UNAUTHORIZED)

        response = Response({"status": msg}, status=status.HTTP_200_OK)
        AuthenticationService.set_refresh_token_cookie(response, data["refresh"])
        AuthenticationService.set_access_token_cookie(response, data["access"])

        return response

    @action(detail=False, methods=["post"])
    def logout(self, request):
        AuthenticationService.logout(request)
        response = Response({"status": "logout successful"})
        AuthenticationService.delete_jwt_token_cookies(response)
        return response

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[AllowAny],
        authentication_classes=[],
        url_path="token/refresh",
        serializer_class=None,
    )
    def refresh_token(self, request):
        try:
            data, msg = AuthenticationService.refresh_token(request)
            if not data:
                return Response({"status": msg}, status=status.HTTP_401_UNAUTHORIZED)

            response = Response({"status": msg}, status=status.HTTP_200_OK)
            AuthenticationService.set_refresh_token_cookie(response, data["refresh"])
            AuthenticationService.set_access_token_cookie(response, data["access"])

            return response
        except TokenError as e:
            return Response(
                {"status": "Invalid or expired token"},
                status=status.HTTP_401_UNAUTHORIZED,
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
