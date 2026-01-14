# drf
from rest_framework.routers import DefaultRouter

# local
from apps.core.views import PagesViewSet

app_name = "apps.core"

router = DefaultRouter()
router.register(r"", PagesViewSet, "pages")
urlpatterns = router.urls
