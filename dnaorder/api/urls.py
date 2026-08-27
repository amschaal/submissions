from rest_framework import routers
from dnaorder.api.viewsets import PIInstitutionViewSet, PIViewSet, SubmissionViewSet, SubmissionFileViewSet,\
    NoteViewSet, SubmissionTypeViewSet, UserViewSet, ValidatorViewSet,\
    DraftViewSet, LabViewSet, ProjectIDViewSet, VocabularyViewset,\
    TermViewSet, ImportViewSet, InstitutionViewSet, UserEmailViewSet,\
    PluginViewSet, TableImportViewSet

router = routers.SimpleRouter()
router.register(r'submissions', SubmissionViewSet)
router.register(r'submission_types', SubmissionTypeViewSet)
router.register(r'submission_files', SubmissionFileViewSet)
router.register(r'notes', NoteViewSet)
router.register(r'users', UserViewSet)
router.register(r'validators', ValidatorViewSet, basename='validators')
router.register(r'drafts', DraftViewSet)
router.register(r'imports', ImportViewSet)
router.register(r'labs', LabViewSet)
router.register(r'institutions', InstitutionViewSet)
router.register(r'project_ids', ProjectIDViewSet)
router.register(r'terms/(?P<vocabulary>[^/.]+)', TermViewSet)
router.register(r'vocabularies', VocabularyViewset)
router.register(r'emails', UserEmailViewSet, basename='emails')
router.register(r'plugins', PluginViewSet, basename='plugins')
router.register(r'tables', TableImportViewSet, basename='tables')
router.register(r'groups', PIViewSet, basename='pis')
router.register(r'group_institutions', PIInstitutionViewSet, basename='group_institutions')


urlpatterns = router.urls