# django
from django.contrib.auth import get_user_model

# drf
from rest_framework import serializers

# local
from apps.payments.models import Order
from apps.products.serializers import ProductSerializer


User = get_user_model()


class OrderSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"


class OrderCreateSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=True, many=False
    )


class OrderPaySerializer(serializers.Serializer):
    pass
