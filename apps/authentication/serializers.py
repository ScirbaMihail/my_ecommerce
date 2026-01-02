from rest_framework import serializers

from django.contrib.auth import get_user_model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(max_digits=6, decimal_places=2)
    class Meta:
        model = User
        fields = '__all__'

class TransactionSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=6, decimal_places=2)