# drf
from rest_framework.routers import DefaultRouter

# local
from apps.authentication.views import UserViewSet, AuthenticationViewSet

app_name = 'apps.authentication'

router = DefaultRouter()
router.register(r"users", UserViewSet, "users")
router.register(r"auth", AuthenticationViewSet, "auth")
urlpatterns = router.urls
