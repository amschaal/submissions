from rest_framework import routers
from dnaorder.api.viewsets import SubmissionViewSet, SubmissionFileViewSet,\
    NoteViewSet, SubmissionTypeViewSet, UserViewSet, ValidatorViewSet,\
    StatusViewSet, DraftViewSet, LabViewSet

router = routers.SimpleRouter()
router.register(r'submissions', SubmissionViewSet)
router.register(r'submission_types', SubmissionTypeViewSet)
router.register(r'submission_files', SubmissionFileViewSet)
router.register(r'notes', NoteViewSet)
router.register(r'users', UserViewSet)
router.register(r'validators', ValidatorViewSet, basename='validators')
router.register(r'statuses', StatusViewSet)
router.register(r'drafts', DraftViewSet)
router.register(r'labs', LabViewSet)

urlpatterns = router.urls