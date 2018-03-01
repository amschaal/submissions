from rest_framework import routers
from dnaorder.api.viewsets import SubmissionViewSet

router = routers.SimpleRouter()
router.register(r'orders', SubmissionViewSet)
urlpatterns = router.urls