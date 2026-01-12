# drf
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

# django
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomTokenObtainSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"detail": "Invalid credentials"})

        if not user.check_password(password):
            raise serializers.ValidationError({"detail": "Invalid credentials"})

        refresh = RefreshToken.for_user(user)

        return {"refresh": str(refresh), "access": str(refresh.access_token)}


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class TransactionSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=6, decimal_places=2)
