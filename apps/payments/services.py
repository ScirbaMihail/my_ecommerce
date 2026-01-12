# django
from django.contrib.auth import get_user_model
from django.db import transaction

# local
from apps.cart.models import Cart
from apps.payments.models import Order, OrderProduct


User = get_user_model()


class OrderService:

    @staticmethod
    def create_order(user):
        try:
            cart = Cart.objects.prefetch_related("products").get(user=user)
            if len(cart.products.all()) == 0:
                return False, {"status": "failed", "message": "Cart is empty"}
        except Cart.DoesNotExist:
            return False, {"status": "failed", "message": "Cart not found"}

        with transaction.atomic():
            order = Order.objects.create(user_id=user, cost=cart.cost)
            cart_products = cart.cartproduct_set.select_related("product")
            OrderProduct.objects.bulk_create(
                [
                    OrderProduct(order=order, product=cp.product, quantity=cp.quantity)
                    for cp in cart_products
                ]
            )

        return True, {
            "status": "success",
            "message": "Order created with pending status",
        }
