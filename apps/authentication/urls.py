# drf
from rest_framework.routers import DefaultRouter

# local
from apps.authentication.views import UserViewSet

app_name = 'apps.authentication'

router = DefaultRouter()
router.register(r"users", UserViewSet, "users")
urlpatterns = router.urls
