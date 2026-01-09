# drf
from rest_framework import serializers

# local
from apps.payments.models import Order
from apps.cart.models import Cart
from apps.products.serializers import ProductSerializer


class OrderSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"


class OrderInputSerializer(serializers.Serializer):
    cart = serializers.PrimaryKeyRelatedField(
        queryset=Cart.objects.prefetch_related("products").all(), required=True
    )
