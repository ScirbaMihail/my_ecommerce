from apps.cart.models import Cart
from apps.products.models import Product


class CartService:

    @staticmethod
    def get_products(serializer, cart_id):
        try:
            cart = Cart.objects.prefetch_related("products").get(id=cart_id)
            data = serializer(cart).data
            return True, {"products": data["products"], "cost": data["cost"]}
        except Cart.DoesNotExist:
            return False, {["Cart not found"]}

    @staticmethod
    def add_product(request, cart_id):
        try:
            # Get cart
            cart = Cart.objects.prefetch_related("products").get(id=cart_id)

            # Get request data
            data = request.POST.data
            product_id, amount = data["product"], data["amount"]

            # Get cart
            product = (Product.objects.select_related("category").get(id=product_id),)

            # Add product into the cart
            cart.products.add(product, through_defaults={"amount": amount})
            return True, {
                "status": "success",
                "message": f"product {product.name=} added to cart",
            }
        except Cart.DoesNotExist:
            return False, {"status": "failed", "message": "cart not found"}
        except Product.DoesNotExist:
            return False, {"status": "failed", "message": "product not found"}
        


            
        
