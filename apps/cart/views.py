# DRF
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

# Django

# Local
from apps.cart.serializers import CartSerializer
from apps.cart.models import Cart
from apps.cart.services import CartService


# Create your views here.
class CartViewSet(ModelViewSet):
    queryset = Cart.objects.prefetch_related('products').all()
    serializer_class = CartSerializer

    @action(detail=True, methods=['get'])
    def items(self, request, pk=None):
        succeeded, response_data = CartService.get_products(self.serializer_class, pk)
        if succeeded:
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(response_data, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def items(self, request, pk=None):
        pass