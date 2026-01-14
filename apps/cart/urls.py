# drf
from rest_framework.routers import DefaultRouter

# local
from apps.cart.views import CartViewSet

app_name = "apps.cart"

router = DefaultRouter()
router.register(r"carts", CartViewSet, basename="carts")

urlpatterns = router.urls
