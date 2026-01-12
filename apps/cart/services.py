# django
from django.db.models import F

# local
from apps.cart.models import Cart, CartProduct
from apps.cart.serializers import CartSerializer
from apps.products.models import Product


class CartService:

    @staticmethod
    def get_items(cart_id):
        try:
            cart = Cart.objects.prefetch_related("products").get(id=cart_id)
            data = CartSerializer(cart)
            return True, {"products": data["products"], "cost": data["cost"]}
        except Cart.DoesNotExist:
            return False, {["cart not found"]}

    @staticmethod
    def add_product(cart_id, data):
        try:
            # Get data
            cart = Cart.objects.prefetch_related("products").get(id=cart_id)
            product, quantity = data["product"], data["quantity"]

            # Add product into the cart
            item, created = CartProduct.objects.get_or_create(
                cart=cart, product=product, defaults={"quantity": quantity}
            )

            if not created:
                item.quantity = F("quantity") + quantity
                item.save(update_fields=["quantity"])
                item.refresh_from_db()

            return True, {
                "status": "success",
                "message": f"product {product.name=} added to cart",
            }
        except Cart.DoesNotExist:
            return False, {"status": "failed", "message": "cart not found"}

    @staticmethod
    def remove_product(cart_id, product_id):
        try:
            cart = Cart.objects.prefetch_related("products").get(id=cart_id)
            product = Product.objects.get(id=product_id)
        except Cart.DoesNotExist:
            return False, {"status": "failed", "message": "cart not found"}
        except Product.DoesNotExist:
            return False, {"status": "failed", "message": "product not found"}

        deleted, _ = CartProduct.objects.filter(cart=cart, product=product).delete()
        if not deleted:
            return False, {
                "status": "failed",
                "message": "product {product.name=} not found in cart",
            }
        return True, {"status": "success", "message": "product deleted"}
