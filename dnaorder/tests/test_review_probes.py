"""Two behaviours a code review of this branch raised, both confirmed and both
waiting on a decision rather than a fix.

Each is marked ``expectedFailure``: the behaviour is real and reproduced here,
so the suite stays green, and if either is changed the run reports an
unexpected success, which is a prompt to settle the test's fate.  Once a
decision is made, each test moves to the file named in its docstring -- either
rewritten to assert the behaviour as intended, or kept as a regression test for
the fix.

The third question from that review (address comparison in code login) is
settled: see test_code_login.ExistingAccountTests.

Run inside the api container:
    docker compose exec api python manage.py test dnaorder.tests.test_review_probes -v 2
"""
import unittest

from allauth.account.models import EmailAddress
from django.contrib.auth.models import User

from dnaorder.tests.base import ApiTestCase
from dnaorder.tests.test_file_fields import FileFieldFixture
from dnaorder.tests.test_payment_required import submission_payload
from dnaorder.utils import assign_submissions


class AccountEmailChangeTests(ApiTestCase):
    """A named user's access when their account email changes.

    Permanent home: dnaorder/tests/test_named_access.py.

    Keycloak's ``user_details`` pipeline step rewrites ``User.email`` at every
    login, so an address change upstream arrives here with the old address
    recorded nowhere.  ``named()`` matches only ``verified_emails(user)``, and
    ``Submission.users`` is a cache rather than a grant (dnaorder/utils.py:29),
    so nothing ties the user to a submission naming their previous address.

    The open question is whether that is intended.  One reading is that the
    address is the identity, and losing it should lose access.  The other is
    that a user who signed in with an address demonstrably controlled it, so
    the social pipeline should record it (as a UserEmail or a verified
    EmailAddress) when it changes -- which
    ``test_keeping_the_old_address_as_a_verified_one_keeps_access`` shows is
    enough to preserve access.
    """

    def detail(self, user):
        return self.as_user(user).get('/api/submissions/{}/'.format(self.sub_a.id))

    def listed_ids(self, user):
        resp = self.as_user(user).get('/api/submissions/')
        return [row['id'] for row in (resp.data or {}).get('results', [])]

    def move_email(self, user, email):
        User.objects.filter(pk=user.pk).update(email=email)
        user.refresh_from_db()

    def test_the_named_submitter_can_open_it_to_begin_with(self):
        # Guards the premise of the two tests below.
        self.assertEqual(self.detail(self.submitter).status_code, 200)
        self.assertIn(self.sub_a.id, self.listed_ids(self.submitter))

    def test_keeping_the_old_address_as_a_verified_one_keeps_access(self):
        old = self.submitter.email
        self.move_email(self.submitter, 'moved@example.com')
        EmailAddress.objects.create(user=self.submitter, email=old, verified=True)
        self.assertEqual(self.detail(self.submitter).status_code, 200)
        self.assertIn(self.sub_a.id, self.listed_ids(self.submitter))

    @unittest.expectedFailure
    def test_access_when_the_old_address_is_recorded_nowhere(self):
        # The users cache as earlier releases populated it, to show whether it
        # still carries any weight.  It does not.
        assign_submissions(self.submitter)
        self.assertTrue(self.sub_a.users.filter(pk=self.submitter.pk).exists())

        self.move_email(self.submitter, 'moved@example.com')

        self.assertEqual(
            self.detail(self.submitter).status_code, 200,
            'the submission still names the old address and Submission.users '
            'still holds the row, but the submission can no longer be opened',
        )
        self.assertIn(
            self.sub_a.id, self.listed_ids(self.submitter),
            'the submission no longer appears in the list either',
        )


class DraftHandoffTests(FileFieldFixture):
    """A draft carrying a form upload, finished by someone other than its owner.

    Permanent home: dnaorder/tests/test_file_fields.py.

    Not in question: an upload belongs to its uploader.  That is deliberate and
    asserted by
    test_file_fields.AttachOnSaveTests.test_upload_can_only_be_used_by_the_user_who_made_it,
    which names pi_user and lab_a_admin among those who may not use it.

    In question: ``DraftPermissions`` says a draft's link works for the people
    it names "so a draft can be handed to a colleague, and for staff helping
    with it".  For a form with a file field the colleague can open the draft,
    but the upload in it is not theirs, so submitting fails on that field --
    with "not found or has expired", for a file that is neither.  The vague
    wording is itself deliberate (file_fields.py:55, so ids cannot be probed),
    so the choice is between narrowing that promise, letting a named user adopt
    the draft's uploads, or having the form clear a file field whose upload
    belongs to someone else and ask for it again.
    """

    def save_draft(self, client, data):
        resp = client.post('/api/drafts/', {'data': data}, format='json')
        self.assertEqual(resp.status_code, 201, resp.content)
        return resp.data['id']

    @unittest.expectedFailure
    def test_a_named_colleague_can_finish_a_draft_holding_an_upload(self):
        file_id = self.upload_id()  # uploaded by self.submitter
        draft_data = {
            'email': self.submitter.email,
            'pi_email': self.pi_user.email,
            'plate': file_id,
        }
        draft_id = self.save_draft(self.as_submitter(), draft_data)

        # The PI is named on the draft, so the link works for them.
        self.assertEqual(
            self.as_user(self.pi_user).get('/api/drafts/{}/'.format(draft_id)).status_code,
            200,
        )

        payload = submission_payload(
            self.type_files,
            submission_data={'plate': file_id},
            email=self.submitter.email,
            pi_email=self.pi_user.email,
        )
        resp = self.as_user(self.pi_user).post('/api/submissions/', payload, format='json')
        self.assertEqual(
            resp.status_code, 201,
            'the PI can open the draft but cannot submit it: {}'.format(resp.content),
        )
