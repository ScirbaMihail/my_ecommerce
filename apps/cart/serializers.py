# DRF
from rest_framework import serializers

# Local
from apps.cart.models import Cart

# Define serializer
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'