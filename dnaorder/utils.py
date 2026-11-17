from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.db.models.query_utils import Q
from django.db.models.functions import Lower
from django.contrib.auth.models import User

def get_site_institution(request):
    from dnaorder.models import Institution
    if settings.MULTI_SITE:
        return Institution.objects.get(site__id=get_current_site(request).id)
    else:
        return Institution.objects.first()
def normalize_emails(emails):
    """Lower-cased, trimmed, de-duplicated; blanks dropped."""
    return sorted({e.strip().lower() for e in emails if e and e.strip()})

def verified_emails(user):
    """Every address the user has proven they control: the account's email, confirmed
    secondary addresses (UserEmail) and addresses verified by an emailed sign-in code.
    This is what decides whether a user is named on a submission (Submission.objects.named)."""
    if not user or not user.is_authenticated:
        return []
    from allauth.account.models import EmailAddress
    emails = [user.email]
    emails.extend(user.emails.values_list('email', flat=True))
    emails.extend(EmailAddress.objects.filter(user=user, verified=True).values_list('email', flat=True))
    return normalize_emails(emails)

# Submission.users is a convenience cache of the accounts named on a submission. It is not
# what grants access: that is decided when the request is made, by Submission.objects.named().
def assign_submissions(user):
    from dnaorder.models import Submission
    for submission in Submission.objects.named(user):
        submission.users.add(user)

def assign_submission(submission):
    from dnaorder.models import UserEmail
    emails = normalize_emails([c.email for c in submission.contacts.all()] + [submission.email, submission.pi_email])
    secondary = UserEmail.objects.alias(lower_email=Lower('email')).filter(lower_email__in=emails).values('user')
    submission.users.set(User.objects.alias(lower_email=Lower('email')).filter(Q(lower_email__in=emails) | Q(pk__in=secondary)))

def get_lab_uri(lab):
    return 'https://{}'.format(lab.institution.site.domain)

def absolute_url(view_name, args=None):
    # Based on BASE_URI like MEDIA_URL: URLs built from the request come out as http:// behind the TLS terminating proxy.
    from django.urls import reverse
    return settings.BASE_URI.rstrip('/') + reverse(view_name, args=args)