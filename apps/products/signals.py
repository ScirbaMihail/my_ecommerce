from django.db.models.signals import pre_save
from django.dispatch import receiver

from apps.products.models import Product


@receiver(pre_save, sender=Product)
def set_in_stock(sender, instance, **kwargs):
    instance.in_stock = True if instance.amount else False
