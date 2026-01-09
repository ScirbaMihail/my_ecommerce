# drf
from rest_framework.viewsets import ModelViewSet

# local
from apps.payments.models import Order
from apps.payments.serializers import OrderSerializer, OrderInputSerializer


# Create your views here.
class OrderViewSet(ModelViewSet):
    queryset = Order.objects.prefetch_related("products").select_related("user").all()
    http_method_names = ("get", "head", "post", "put", "patch")
    serializer_class = OrderSerializer
