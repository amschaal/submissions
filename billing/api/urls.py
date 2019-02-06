from rest_framework import routers
from billing.api.viewsets import ServiceViewSet, LineItemViewSet

router = routers.SimpleRouter()
router.register(r'services', ServiceViewSet)
router.register(r'line_items', LineItemViewSet)

urlpatterns = router.urls