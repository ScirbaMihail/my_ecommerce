from apps.cart.models import Cart, CartProduct
from apps.cart.serializers import CartSerializer
from django.db.models import F


class CartService:

    @staticmethod
    def get_items(cart_id):
        try:
            cart = Cart.objects.prefetch_related("products").get(id=cart_id)
            data = CartSerializer(cart) 
            return True, {"products": data["products"], "cost": data["cost"]}
        except Cart.DoesNotExist:
            return False, {['cart not found']} 

    @staticmethod
    def add_product(cart_id, data):
        try:
            # Get data
            cart = Cart.objects.prefetch_related("products").get(id=cart_id)
            product, quantity = data["product"], data["quantity"]

            # Add product into the cart
            item, created = CartProduct.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': quantity}
            )

            if not created:
                item.quantity = F('quantity') + quantity
                item.save(update_fields=['quantity'])
                item.refresh_from_db()

            return True, {
                "status": "success",
                "message": f"product {product.name=} added to cart",
            }
        except Cart.DoesNotExist:
            return False, {"status": "failed", "message": "cart not found"}
