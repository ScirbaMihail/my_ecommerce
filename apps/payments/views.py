# drf
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

# local
from apps.payments.models import Order
from apps.payments.serializers import OrderSerializer, OrderInputSerializer
from apps.payments.services import OrderService


# Create your views here.
class OrderViewSet(ModelViewSet):
    queryset = Order.objects.prefetch_related("products").select_related("user").all()
    http_method_names = ("get", "head", "post")
    serializer_class = OrderSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return OrderInputSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        succeeded, response = OrderService.create_order(user=request.data["user"])
        return Response(
            response,
            status=status.HTTP_201_CREATED if succeeded else status.HTTP_404_NOT_FOUND,
        )
