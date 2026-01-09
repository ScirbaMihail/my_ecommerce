from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

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

    class Currencies(models.TextChoices):
        MDL = "mdl", _("MDL")
        EUR = "eur", _("EUR")
        USD = "usd", _("USD")

    class Statuses(models.TextChoices):
        SUCCESS = "success", _("Success")
        FAIL = "fail", _("Fail")

    order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, blank=False, on_delete=models.SET_NULL)
    amount = models.PositiveIntegerField()
    currency = models.CharField(
        max_length=3, choices=Currencies.choices, default=Currencies.MDL
    )
    status = models.CharField(choices=Statuses.choices)
