# DRF
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

# Django

# Local
from apps.cart.serializers import CartSerializer
from apps.cart.models import Cart


# Create your views here.
class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    @action(detail=True, methods=['get'])
    def items(self, request, pk=None):
        try:
            cart = Cart.objects.prefetch_related('products').get(id=pk)
            data = self.get_serializer(cart).data
            return Response({'products': data['products'], 'cost': data['cost']}, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({'status': 'not found'}, status=status.HTTP_404_NOT_FOUND)
        