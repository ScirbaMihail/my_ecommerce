from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

# Create your models here.
class Category(models.Model):
    name = models.CharField(unique=True)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'categories'


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(null=False, blank=True)
    price = models.FloatField(validators=[MinValueValidator(0)])
    amount = models.PositiveIntegerField()
    in_stock = models.BooleanField(blank=True)
    category = models.ForeignKey(to=Category, null=True, blank=False, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'products'