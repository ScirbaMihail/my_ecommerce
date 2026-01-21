# drf
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

# django
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomTokenObtainSerializer(serializers.Serializer):
    """
    Custom Token Serializer which create token by validating user
    with email instead of username.
    """

    # Fields what have to be passed for token
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class PerformTransactionSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=6, decimal_places=2)
