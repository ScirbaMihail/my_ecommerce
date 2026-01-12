# drf
from rest_framework.routers import DefaultRouter

# local
from apps.payments.views import OrderViewSet

router = DefaultRouter()
router.register("payments/orders", OrderViewSet, basename="orders")
urlpatterns = router.urls
