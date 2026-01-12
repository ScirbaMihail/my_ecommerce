# django
from django.db.models.signals import pre_save
from django.dispatch import receiver

# local
from apps.products.models import Product, Category


@receiver(pre_save, sender=Product)
def set_in_stock(sender, instance, **kwargs):
    instance.in_stock = True if instance.amount else False


@receiver(pre_save, sender=Category)
def capitalize_name(sender, instance, **kwargs):
    instance.name = instance.name.lower().capitalize()
