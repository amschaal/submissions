from rest_framework import routers
from dnaorder.api.viewsets import SubmissionViewSet, SubmissionFileViewSet,\
    NoteViewSet, SubmissionTypeViewSet, UserViewSet

router = routers.SimpleRouter()
router.register(r'submissions', SubmissionViewSet)
router.register(r'submission_types', SubmissionTypeViewSet)
router.register(r'submission_files', SubmissionFileViewSet)
router.register(r'notes', NoteViewSet)
router.register(r'users', UserViewSet)

urlpatterns = router.urls