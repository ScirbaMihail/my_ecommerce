from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

from apps.products.models import Product

User = get_user_model()


# Create your models here.
class Order(models.Model):

    class Statuses(models.TextChoices):
        PENDING = "pending", _("Pending")
        PAID = "paid", _("Paid")
        CANCELED = "canceled", _("Canceled")

    user = models.ForeignKey(User, null=True, blank=False, on_delete=models.SET_NULL)
    products = models.ManyToManyField(Product, through="OrderProduct")
    cost = models.PositiveIntegerField()
    status = models.CharField(choices=Statuses.choices, default=Statuses.PENDING)


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, blank=False, on_delete=models.SET_NULL)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=1)
