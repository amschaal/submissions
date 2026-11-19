"""Who is "named" on a submission, and which submissions a user may open by id.

``Submission.objects.named(user)`` and ``.visible_to(user)`` are the single
definition the API builds its access rules on.
"""
from allauth.account.models import EmailAddress

from dnaorder.models import Contact, Submission, UserEmail
from dnaorder.tests.base import ApiTestCase, make_participant, make_submission, make_user
from dnaorder.utils import assign_submission, verified_emails


class NamedTests(ApiTestCase):
    def named_ids(self, user):
        return set(Submission.objects.named(user).values_list("id", flat=True))

    def test_submitter_and_pi_are_named(self):
        everything = {self.sub_a.id, self.sub_a_locked.id, self.sub_b.id}
        self.assertEqual(self.named_ids(self.submitter), everything)
        self.assertEqual(self.named_ids(self.pi_user), everything)

    def test_contact_is_named_on_that_submission_only(self):
        self.assertEqual(self.named_ids(self.contact_user), {self.sub_a.id})
        colleague = make_user("colleague", email="colleague@example.com")
        self.assertEqual(self.named_ids(colleague), set())
        Contact.objects.create(submission=self.sub_b, first_name="Col", last_name="League", email="Colleague@Example.com")
        self.assertEqual(self.named_ids(colleague), {self.sub_b.id})

    def test_matching_ignores_case_and_surrounding_space(self):
        other = make_submission(self.type_a, email="Mixed.Case@Example.com", pi_email="x@example.com")
        user = make_user("mixed", email=" mixed.case@EXAMPLE.com ")
        self.assertEqual(self.named_ids(user), {other.id})

    def test_confirmed_secondary_address_counts(self):
        user = make_user("second", email="second@example.com")
        self.assertEqual(self.named_ids(user), set())
        UserEmail.objects.create(user=user, email="PI@example.com")
        self.assertIn(self.sub_a.id, self.named_ids(user))

    def test_address_verified_by_sign_in_code_counts(self):
        other = make_submission(self.type_a, email="old@example.com", pi_email="x@example.com")
        user = make_user("moved", email="new@example.com")
        EmailAddress.objects.create(user=user, email="old@example.com", verified=True)
        self.assertEqual(self.named_ids(user), {other.id})

    def test_unverified_code_address_does_not_count(self):
        make_submission(self.type_a, email="old@example.com", pi_email="x@example.com")
        user = make_user("pending", email="new@example.com")
        EmailAddress.objects.create(user=user, email="old@example.com", verified=False)
        self.assertEqual(self.named_ids(user), set())

    def test_user_without_email_is_named_on_nothing(self):
        make_submission(self.type_a, email="someone@example.com", pi_email="")
        self.assertEqual(verified_emails(make_user("blank")), [])
        self.assertEqual(self.named_ids(make_user("blank2")), set())

    def test_unrelated_user_is_named_on_nothing(self):
        self.assertEqual(self.named_ids(self.outsider), set())
        self.assertFalse(self.sub_a.is_named(self.outsider))


class VisibleToTests(ApiTestCase):
    def visible_ids(self, user):
        return set(Submission.objects.visible_to(user).values_list("id", flat=True))

    def test_anonymous_sees_nothing(self):
        from django.contrib.auth.models import AnonymousUser
        self.assertEqual(self.visible_ids(AnonymousUser()), set())

    def test_unrelated_user_sees_nothing(self):
        self.assertEqual(self.visible_ids(self.outsider), set())
        self.assertFalse(self.sub_a.is_visible_to(self.outsider))

    def test_superuser_sees_everything(self):
        self.assertEqual(self.visible_ids(self.superuser), {self.sub_a.id, self.sub_a_locked.id, self.sub_b.id})

    def test_lab_staff_see_their_lab_only(self):
        lab_a = {self.sub_a.id, self.sub_a_locked.id}
        self.assertEqual(self.visible_ids(self.lab_a_member), lab_a)
        self.assertEqual(self.visible_ids(self.lab_a_associate), lab_a)
        self.assertEqual(self.visible_ids(self.lab_b_member), {self.sub_b.id})

    def test_institution_admin_sees_the_institution(self):
        self.assertEqual(self.visible_ids(self.inst_admin), {self.sub_a.id, self.sub_a_locked.id, self.sub_b.id})

    def test_participant_sees_the_submission(self):
        make_participant(self.sub_b, self.outsider)
        self.assertEqual(self.visible_ids(self.outsider), {self.sub_b.id})

    def test_named_user_sees_the_submission(self):
        self.assertEqual(self.visible_ids(self.contact_user), {self.sub_a.id})
        Contact.objects.create(submission=self.sub_b, first_name="O", last_name="Ut", email="OUT@example.com")
        self.assertEqual(self.visible_ids(self.outsider), {self.sub_b.id})
        self.assertTrue(self.sub_b.is_visible_to(self.outsider))

    def test_lab_staff_named_elsewhere_see_both(self):
        Contact.objects.create(submission=self.sub_b, first_name="A", last_name="M", email=self.lab_a_member.email)
        self.assertEqual(self.visible_ids(self.lab_a_member), {self.sub_a.id, self.sub_a_locked.id, self.sub_b.id})


class UsersCacheTests(ApiTestCase):
    """``Submission.users`` mirrors who is named; it is kept for listing, not for access."""

    def test_new_account_is_linked_without_resaving_submissions(self):
        submission = make_submission(self.type_a, email="later@example.com", pi_email="x@example.com")
        before = Submission.objects.get(pk=submission.pk).updated
        user = make_user("later", email="LATER@example.com")
        self.assertIn(user, submission.users.all())
        self.assertEqual(Submission.objects.get(pk=submission.pk).updated, before)

    def test_assign_submission_matches_case_insensitively_and_secondary_addresses(self):
        submission = make_submission(self.type_a, email="Primary@Example.com", pi_email="Second@Example.com")
        primary = make_user("primary", email="primary@example.com")
        secondary = make_user("secondary", email="other@example.com")
        UserEmail.objects.create(user=secondary, email="second@example.com")
        submission.users.clear()
        assign_submission(submission)
        self.assertEqual(set(submission.users.all()), {primary, secondary})
