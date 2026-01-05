# Django
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

# Local
from apps.products.models import Product

User = get_user_model()


# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through="CartProduct")
    cost = models.DecimalField(validators=[MinValueValidator(0)], max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = 'carts'

class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, blank=False, on_delete=models.SET_NULL)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        db_table = 'carts_products'
        unique_together = ['cart', 'product']
        ordering = ['product__name']