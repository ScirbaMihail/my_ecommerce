# django
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum, F
from django.contrib.auth import get_user_model

# local
from apps.cart.models import CartProduct, Cart


User = get_user_model()


@receiver(post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)


@receiver([post_save, post_delete], sender=CartProduct)
def update_cart_cost(sender, instance, **kwargs):
    cart = instance.cart
    total = (
        CartProduct.objects.filter(cart=cart).aggregate(
            total=Sum(F("product__price") * F("quantity"))
        )["total"]
        or 0
    )

    cart.cost = total
    cart.save(update_fields=["cost"])
