# django
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

# local
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
    product = models.ForeignKey(
        Product, null=True, blank=False, on_delete=models.SET_NULL
    )
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=1)


class Transaction(models.Model):
    class Status(models.TextChoices):
        FAIL = "fail", _("Fail")
        SUCCESS = "success", _("Success")

    order = models.ForeignKey(Order, null=True, blank=False, on_delete=models.SET_NULL)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(choices=Status.choices)
