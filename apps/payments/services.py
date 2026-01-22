# django
from django.contrib.auth import get_user_model
from django.db import transaction as tr

# local
from apps.cart.models import Cart
from apps.payments.models import Order, OrderProduct, Transaction


User = get_user_model()


class OrderService:

    @staticmethod
    def create_order(user):
        try:
            cart = Cart.objects.prefetch_related("products").get(user=user)
        except Cart.DoesNotExist:
            return False, {"status": "failed", "message": "Cart not found"}

        if len(cart.products.all()) == 0:
            return False, {"status": "failed", "message": "Cart is empty"}

        with tr.atomic():
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

    @staticmethod
    def process_payment(order_id: int):
        # Validations
        try:
            order = Order.objects.select_related("user", "user__cart").get(pk=order_id)
        except Order.DoesNotExist:
            return False, {"status": "fail", "message": "Order does not exist"}

        if order.status != order.Statuses.PENDING:
            return False, {
                "status": "fail",
                "message": f"Order is already {order.status}",
            }

        # Payment process
        with tr.atomic():
            transaction = Transaction(order=order, amount=order.cost)

            # Case with not enough money
            if order.user.balance < order.cost:
                order.status = order.Statuses.CANCELED
                order.save(update_fields=["status"])
                transaction.status = transaction.Status.FAIL
                transaction.save()
                return False, {"status": "fail", "message": "Not enough money"}

            cart = order.user.cart
            cart.products.clear()

            order.user.balance -= order.cost
            order.user.save(update_fields=["balance"])

            transaction.status = transaction.Status.SUCCESS
            transaction.save()

            order.status = order.Statuses.PAID
            order.save(update_fields=["status"])

        return True, {"status": "success", "message": "Order is paid"}

    @staticmethod
    def mark_paid(order_id: int):
        try:
            order = Order.objects.get(pk=order_id)
            order.status = Order.Statuses.PAID
            order.save(update_fields=["status"])
            return True, {"status": "success", "message": "order marked as paid"}
        except Order.DoesNotExist:
            return False, {"status": "failed", "message": "order does not exist"}
