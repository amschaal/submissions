from rest_framework import routers
from dnaorder.api.viewsets import SubmissionViewSet, SubmissionFileViewSet,\
    NoteViewSet

router = routers.SimpleRouter()
router.register(r'submissions', SubmissionViewSet)
router.register(r'submission_files', SubmissionFileViewSet)
router.register(r'notes', NoteViewSet)

urlpatterns = router.urls