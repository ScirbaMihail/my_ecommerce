# django
from django.shortcuts import redirect
from django.urls import reverse_lazy

# drf
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

# local
from apps.payments.models import Order, Transaction
from apps.payments.serializers import (
    OrderSerializer,
    OrderCreateSerializer,
    OrderPaySerializer,
    TransactionSerializer,
)
from apps.payments.services import OrderService


# Create your views here.
class OrderViewSet(ModelViewSet):
    queryset = Order.objects.prefetch_related("products").select_related("user").all()
    http_method_names = ("get", "head", "post")
    serializer_class = OrderSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return OrderCreateSerializer
        elif self.action == "pay":
            return OrderPaySerializer
        return super().get_serializer_class()

    def create(self, request: Request, *args, **kwargs):
        succeeded, response = OrderService.create_order(user=request.data["user"])
        return Response(
            response,
            status=status.HTTP_201_CREATED if succeeded else status.HTTP_404_NOT_FOUND,
        )

    @action(detail=True, methods=["post"])
    def pay(self, request: Request, pk=None):
        succeeded, response = OrderService.process_payment(pk)
        return Response(
            response,
            status=status.HTTP_201_CREATED if succeeded else status.HTTP_404_NOT_FOUND,
        )


class TransactionViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
