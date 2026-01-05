# DRF
from rest_framework.viewsets import ModelViewSet

# Django

# Local
from apps.cart.serializers import CartSerializer
from apps.cart.models import Cart


# Create your views here.
class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer