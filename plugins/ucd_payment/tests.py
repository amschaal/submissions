"""The ucd_payment plugin: payment by UC Davis chartstring or purchase order, and nothing else."""
from unittest import mock

import requests
from django.test import SimpleTestCase, override_settings

from dnaorder.models import Submission
from dnaorder.tests.base import ApiTestCase
from dnaorder.tests.test_payment_required import submission_payload
from plugins import PluginManager

from . import aggie_enterprise
from .chartstring import GL, PPM, complete_gl, parse
from .plugin import UCDPaymentPlugin

GL_SHORT = '3110-FUND1-DEPT001-500000'
GL_FULL = '3110-FUND1-DEPT001-500000-62-PRG-PROJECT001-ACT001-0000-000000-000000'
PPM_PTOE = 'PROJECT001-TASK01-ORGCODE-EXP001'
PPM_POET = 'PROJECT001-ORGCODE-EXP001-TASK01'
CONTACT = {"financial_contact_name": "Fiona Fiscal", "financial_contact_email": "fiscal@example.edu"}
#: Aggie Enterprise's GlSegmentString format.
AE_GL_REGEX = (r'^[0-9]{3}[0-9AB]-[0-9A-Z]{5}-[0-9A-Z]{7}-[0-9A-Z]{6}-[0-9][0-9A-Z]-[0-9A-Z]{3}-[0-9A-Z]{10}'
               r'-[0-9A-Z]{6}-0000-000000-000000$')


class ParseChartstringTests(SimpleTestCase):
    def test_gl_strings_need_only_the_first_four_segments(self):
        for value in [GL_SHORT, '3110-FUND1-DEPT001-500000-62-PRG-PROJECT001-ACT001', GL_FULL]:
            with self.subTest(value=value):
                self.assertEqual(parse(value), (GL, value))

    def test_whitespace_is_ignored_and_codes_upper_cased(self):
        self.assertEqual(parse(' 3110 - fund1-dept001-500000\n'), (GL, GL_SHORT))
        self.assertEqual(parse('project001-task01-orgcode-exp001'), (PPM, PPM_PTOE))

    def test_ppm_strings_have_four_or_six_segments(self):
        self.assertEqual(parse(PPM_PTOE), (PPM, PPM_PTOE))
        self.assertEqual(parse(PPM_PTOE + '-AWARD01-FUND01'), (PPM, PPM_PTOE + '-AWARD01-FUND01'))

    def test_funding_source_keeps_its_case(self):
        self.assertEqual(parse(PPM_PTOE.lower() + '-award01-Fund01').string, PPM_PTOE + '-AWARD01-Fund01')

    def test_poet_order_is_put_in_aggie_enterprise_order(self):
        self.assertEqual(parse(PPM_POET), (PPM, PPM_PTOE))
        self.assertEqual(parse(PPM_POET + '-AWARD01-FUND01'), (PPM, PPM_PTOE + '-AWARD01-FUND01'))

    def test_all_zero_award_and_funding_source_are_dropped(self):
        # Finjector's POET form fills a missing Award and Funding Source with zeroes.
        self.assertEqual(parse(PPM_POET + '-0000000-00000'), (PPM, PPM_PTOE))

    def test_invalid_strings_say_what_is_wrong(self):
        cases = {
            '': 'Please enter a GL chartstring',
            'not a chartstring': 'Please enter a GL chartstring',
            '3110-FUND1-DEPT001': 'A GL chartstring is',
            GL_FULL + '-000000': 'A GL chartstring is',
            '3110-FUND1-DEPT01-500000': '"DEPT01" is not a valid Financial Department',
            '311C-FUND1-DEPT001-500000': '"311C" is not a valid Entity',
            GL_FULL.replace('-0000-', '-1234-'): '"1234" is not a valid Inter-Entity',
            PPM_PTOE + '-AWARD01': 'A PPM chartstring is',
            'PROJECT001-TASK1-ORGCODE-EXP001': '"TASK1" is not a valid Task',
            PPM_PTOE + '-AWARD1-FUND01': '"AWARD1" is not a valid Award',
        }
        for value, message in cases.items():
            with self.subTest(value=value), self.assertRaisesMessage(ValueError, message):
                parse(value)

    def test_gl_strings_complete_with_zeroes(self):
        self.assertEqual(complete_gl(GL_SHORT), GL_SHORT + '-00-000-0000000000-000000-0000-000000-000000')
        self.assertEqual(complete_gl(GL_FULL), GL_FULL)
        for value in [GL_SHORT, '3110-FUND1-DEPT001-500000-62', GL_FULL]:
            self.assertRegex(complete_gl(value), AE_GL_REGEX)


@override_settings(AGGIE_ENTERPRISE_GRAPHQL_URL='')  # tests never reach a real Aggie Enterprise
class UCDPaymentFixture(ApiTestCase):
    """The standard fixture, with Lab A taking payment through the ucd_payment plugin."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.lab_a.payment_type_id = UCDPaymentPlugin.ID
        cls.lab_a.save()

    def setUp(self):
        super().setUp()
        # Whether or not the plugin is in this environment's PLUGINS.
        patcher = mock.patch.dict(PluginManager().payment_types, {UCDPaymentPlugin.ID: UCDPaymentPlugin.PAYMENT})
        patcher.start()
        self.addCleanup(patcher.stop)
        aggie_enterprise.forget_token()

    def post(self, payment):
        """Submit `payment`, with a valid financial contact unless it gives its own."""
        payment = dict(CONTACT, **payment)
        return self.as_anon().post("/api/submissions/", submission_payload(self.type_a, payment=payment), format="json")


class UCDPaymentTests(UCDPaymentFixture):
    def test_chartstring_is_stored_in_canonical_form(self):
        resp = self.post({"payment_type": "DaFIS", "payment_info": PPM_POET.lower()})
        self.assertEqual(resp.status_code, 201, resp.content)
        payment = Submission.objects.get(pk=resp.data["id"]).payment
        self.assertEqual(
            payment, dict(CONTACT, plugin_id="ucd_payment", payment_type="DaFIS", payment_info=PPM_PTOE)
        )
        self.assertEqual(resp.data["payment"]["display"], {
            "Payment Type": "UC Davis chartstring", "Chartstring": PPM_PTOE,
            "Financial Contact": "Fiona Fiscal", "Financial Contact Email": "fiscal@example.edu",
        })

    def test_purchase_order_is_accepted(self):
        resp = self.post({"payment_type": "Purchase Order", "payment_info": " PO-1234 "})
        self.assertEqual(resp.status_code, 201, resp.content)
        self.assertEqual(Submission.objects.get(pk=resp.data["id"]).payment["payment_info"], "PO-1234")
        self.assertEqual(resp.data["payment"]["display"], {
            "Payment Type": "Purchase Order", "PO Number": "PO-1234",
            "Financial Contact": "Fiona Fiscal", "Financial Contact Email": "fiscal@example.edu",
        })

    def test_financial_contact_is_required(self):
        for payment_type, payment_info in [("DaFIS", GL_SHORT), ("Purchase Order", "PO-1")]:
            with self.subTest(payment_type=payment_type):
                resp = self.post({
                    "payment_type": payment_type, "payment_info": payment_info,
                    "financial_contact_name": "", "financial_contact_email": "",
                })
                self.assertEqual(resp.status_code, 400, resp.content)
                self.assertEqual(set(resp.data["payment"]), {"financial_contact_name", "financial_contact_email"})

    def test_financial_contact_email_must_be_an_email_address(self):
        resp = self.post({"payment_type": "Purchase Order", "payment_info": "PO-1", "financial_contact_email": "Fiona"})
        self.assertEqual(resp.status_code, 400, resp.content)
        self.assertIn("financial_contact_email", resp.data["payment"])

    def test_every_problem_is_reported_at_once(self):
        resp = self.post({"payment_type": "DaFIS", "payment_info": "3110-FUND1", "financial_contact_name": ""})
        self.assertEqual(resp.status_code, 400, resp.content)
        self.assertEqual(set(resp.data["payment"]), {"payment_info", "financial_contact_name"})

    def test_other_payment_types_are_rejected(self):
        for payment_type in ["Credit Card", "UC Chart String", ""]:
            with self.subTest(payment_type=payment_type):
                resp = self.post({"payment_type": payment_type, "payment_info": "anything"})
                self.assertEqual(resp.status_code, 400, resp.content)
                self.assertIn("payment_type", resp.data["payment"])

    def test_payment_type_is_required(self):
        resp = self.post({"payment_info": "PO-1"})
        self.assertEqual(resp.status_code, 400, resp.content)
        self.assertIn("payment_type", resp.data["payment"])

    def test_submission_without_payment_reads_as_empty(self):
        # e.g. one from before the lab took payment through this plugin.
        resp = self.as_user(self.lab_a_member).get("/api/submissions/{}/".format(self.sub_a.id))
        self.assertEqual(resp.status_code, 200, resp.content)
        self.assertEqual(resp.data["payment"], {})

    def test_payment_info_is_required(self):
        for payment_type in ["DaFIS", "Purchase Order"]:
            with self.subTest(payment_type=payment_type):
                resp = self.post({"payment_type": payment_type, "payment_info": ""})
                self.assertEqual(resp.status_code, 400, resp.content)
                self.assertIn("payment_info", resp.data["payment"])

    def test_malformed_chartstring_is_rejected(self):
        resp = self.post({"payment_type": "DaFIS", "payment_info": "3110-FUND1-DEPT01-500000"})
        self.assertEqual(resp.status_code, 400, resp.content)
        self.assertIn('"DEPT01" is not a valid Financial Department', resp.data["payment"]["payment_info"][0])

    def test_payment_cannot_name_another_plugin(self):
        resp = self.post({"plugin_id": "ppms", "payment_type": "Purchase Order", "payment_info": "PO-1"})
        self.assertEqual(resp.status_code, 201, resp.content)
        self.assertEqual(Submission.objects.get(pk=resp.data["id"]).payment["plugin_id"], "ucd_payment")

    def test_aggie_enterprise_is_not_asked_unless_configured(self):
        with mock.patch("plugins.ucd_payment.aggie_enterprise.requests.post") as post:
            resp = self.post({"payment_type": "DaFIS", "payment_info": GL_SHORT})
        self.assertEqual(resp.status_code, 201, resp.content)
        post.assert_not_called()


AE_SETTINGS = {
    "AGGIE_ENTERPRISE_GRAPHQL_URL": "https://ae.example.edu/graphql",
    "AGGIE_ENTERPRISE_TOKEN_URL": "https://ae.example.edu/oauth2/token",
    "AGGIE_ENTERPRISE_CONSUMER_KEY": "key",
    "AGGIE_ENTERPRISE_CONSUMER_SECRET": "secret",
    "AGGIE_ENTERPRISE_SCOPE": "coreomics-test",
}


def fake_response(body):
    response = mock.Mock(status_code=200)
    response.json.return_value = body
    return response


class FakeAggieEnterprise:
    """Stands in for requests.post: hands out a token, and answers validation queries with `result`
    (a validationResponse, or an exception to raise)."""

    def __init__(self, result):
        self.result = result
        self.token_requests = []
        self.queries = []

    def __call__(self, url, **kwargs):
        if url == AE_SETTINGS["AGGIE_ENTERPRISE_TOKEN_URL"]:
            self.token_requests.append(kwargs)
            return fake_response({"access_token": "token", "expires_in": 3600})
        self.queries.append(kwargs)
        if isinstance(self.result, Exception):
            raise self.result
        answer = {"validationResponse": self.result}
        return fake_response({"data": {"glValidateChartstring": answer, "ppmSegmentStringValidate": answer}})


VALID = {"valid": True, "errorMessages": []}


@override_settings(**AE_SETTINGS)
class AggieEnterpriseValidationTests(UCDPaymentFixture):
    def fake_aggie_enterprise(self, result):
        fake = FakeAggieEnterprise(result)
        patcher = mock.patch("plugins.ucd_payment.aggie_enterprise.requests.post", side_effect=fake)
        patcher.start()
        self.addCleanup(patcher.stop)
        return fake

    def test_gl_chartstring_is_validated_in_full(self):
        fake = self.fake_aggie_enterprise(VALID)
        resp = self.post({"payment_type": "DaFIS", "payment_info": GL_SHORT})
        self.assertEqual(resp.status_code, 201, resp.content)
        [query] = fake.queries
        self.assertIn("glValidateChartstring", query["json"]["query"])
        self.assertEqual(query["json"]["variables"], {"segmentString": complete_gl(GL_SHORT), "validateCVRs": True})
        self.assertEqual(query["headers"], {"Authorization": "Bearer token"})
        # What was entered is what's stored.
        self.assertEqual(Submission.objects.get(pk=resp.data["id"]).payment["payment_info"], GL_SHORT)

    def test_ppm_chartstring_is_validated_in_aggie_enterprise_order(self):
        fake = self.fake_aggie_enterprise(VALID)
        resp = self.post({"payment_type": "DaFIS", "payment_info": PPM_POET})
        self.assertEqual(resp.status_code, 201, resp.content)
        [query] = fake.queries
        self.assertIn("ppmSegmentStringValidate", query["json"]["query"])
        self.assertEqual(query["json"]["variables"], {"segmentString": PPM_PTOE})

    def test_aggie_enterprise_errors_are_shown(self):
        self.fake_aggie_enterprise({"valid": False, "errorMessages": ["Fund FUND1 is inactive."]})
        resp = self.post({"payment_type": "DaFIS", "payment_info": GL_SHORT})
        self.assertEqual(resp.status_code, 400, resp.content)
        self.assertEqual(resp.data["payment"]["payment_info"], ["Fund FUND1 is inactive."])

    def test_unavailable_aggie_enterprise_does_not_block_submissions(self):
        self.fake_aggie_enterprise(requests.ConnectionError())
        with self.assertLogs("plugins.ucd_payment", "WARNING"):
            resp = self.post({"payment_type": "DaFIS", "payment_info": GL_SHORT})
        self.assertEqual(resp.status_code, 201, resp.content)

    def test_token_is_requested_once_and_reused(self):
        fake = self.fake_aggie_enterprise(VALID)
        for _ in range(2):
            resp = self.post({"payment_type": "DaFIS", "payment_info": GL_SHORT})
            self.assertEqual(resp.status_code, 201, resp.content)
        [token_request] = fake.token_requests
        self.assertEqual(token_request["auth"], ("key", "secret"))
        self.assertEqual(token_request["data"], {"grant_type": "client_credentials", "scope": "coreomics-test"})
        self.assertEqual(len(fake.queries), 2)

    def test_purchase_orders_are_not_sent_to_aggie_enterprise(self):
        fake = self.fake_aggie_enterprise(VALID)
        resp = self.post({"payment_type": "Purchase Order", "payment_info": "PO-1"})
        self.assertEqual(resp.status_code, 201, resp.content)
        self.assertEqual(fake.queries, [])

    def test_unchanged_payment_is_not_validated_again(self):
        fake = self.fake_aggie_enterprise(VALID)
        resp = self.post({"payment_type": "DaFIS", "payment_info": GL_SHORT})
        self.assertEqual(resp.status_code, 201, resp.content)
        url = "/api/submissions/{}/".format(resp.data["id"])
        given = self.as_user(self.lab_a_admin).get(url).data["payment"]
        resp = self.as_user(self.lab_a_admin).put(url, submission_payload(self.type_a, payment=given), format="json")
        self.assertEqual(resp.status_code, 200, resp.content)
        self.assertEqual(len(fake.queries), 1)
