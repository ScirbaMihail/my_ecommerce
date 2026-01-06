# DRF
from rest_framework import serializers

# Local
from apps.cart.models import Cart
from apps.products.serializers import ProductSerializer
from apps.products.models import Product

# Define serializer
class CartSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'


class CartItemInputSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=True)
    quantity = serializers.IntegerField(min_value=1, required=True)
