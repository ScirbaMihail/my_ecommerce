# drf
from rest_framework.routers import DefaultRouter

# local
from apps.payments.views import OrderViewSet, TransactionViewSet

router = DefaultRouter()
router.register("payments/orders", OrderViewSet, basename="orders")
router.register("payments/transaction", TransactionViewSet, basename="transactions")
urlpatterns = router.urls
