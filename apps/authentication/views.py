# django
from django.contrib.auth import get_user_model

# drf
from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

# local
from apps.authentication.services import UserService
from apps.authentication.serializers import (
    TransactionSerializer,
    UserSerializer,
    CustomTokenObtainSerializer,
)

User = get_user_model()


# Create your views here.
class CustomTokenObtainView(APIView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class UserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action in ["deposit", "withdraw"]:
            return TransactionSerializer
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
