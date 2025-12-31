from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from apps.products.serializers import ProductSerializer
from apps.products.models import Product

# Create your views here.
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer