from rest_framework import serializers

class TransactionSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=6, decimal_places=2)