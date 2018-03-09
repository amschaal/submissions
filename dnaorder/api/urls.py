from rest_framework import routers
from dnaorder.api.viewsets import SubmissionViewSet, SubmissionFileViewSet

router = routers.SimpleRouter()
router.register(r'orders', SubmissionViewSet)
router.register(r'submission_files', SubmissionFileViewSet)
urlpatterns = router.urls