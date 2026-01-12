# drf
from rest_framework import serializers

# local
from apps.products.models import Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        exclude = ("in_stock",)
