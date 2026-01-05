# DRF
from rest_framework import serializers

# Local
from apps.cart.models import Cart
from apps.products.serializers import ProductSerializer

# Define serializer
class CartSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'