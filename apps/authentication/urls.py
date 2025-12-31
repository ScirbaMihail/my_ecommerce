from rest_framework.routers import DefaultRouter

from apps.authentication.views import UserTransactionViewSet

router = DefaultRouter()
router.register(r'users', UserTransactionViewSet, 'users')
urlpatterns = router.urls