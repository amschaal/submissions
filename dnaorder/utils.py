from django.contrib.sites.shortcuts import get_current_site
from django.db.models.query_utils import Q
from django.contrib.auth.models import User

def get_site_institution(request):
    from dnaorder.models import Institution
    return Institution.objects.get(site__id=get_current_site(request).id)

def assign_submissions(user):
    from dnaorder.models import Submission
    for submission in Submission.objects.filter(Q(pi_email__iexact=user.email)|Q(email__iexact=user.email)|Q(contacts__email__iexact=user.email)).distinct():
        submission.users.add(user)
        submission.save()

def assign_submission(submission):
    emails = [c.email for c in submission.contacts.all()] + [submission.email, submission.pi_email]
    submission.users.set(User.objects.filter(email__in=emails))

def get_lab_uri(lab):
    return 'https://{}'.format(lab.institution.site.domain)