from rest_framework.routers import DefaultRouter

from apps.authentication.views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, 'users')
urlpatterns = router.urls