from rest_framework import routers
from .views import TotalsViewSet

router = routers.DefaultRouter()
router.register('totals', TotalsViewSet, basename='totals')

urlpatterns = router.urls
