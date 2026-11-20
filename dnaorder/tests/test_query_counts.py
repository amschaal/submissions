"""How the submissions list and export scale: queries per additional row.

The absolute query count for a page is not very interesting -- it moves
whenever a prefetch is added or a filter changes.  What matters is the marginal
cost: how many queries each extra row costs.  A healthy endpoint is flat (0 per
row), because every row is served from rows already fetched
(SubmissionViewSet.preload).

The rows are seeded the way real ones look -- a mapped PI with an institution,
a receiver, a contact and participants -- because each of those is something
the list serializer renders per row.  A bare row would hide them.

On failure the message breaks the cost down by query shape, so the queries that
repeat per row can be addressed individually.

Run inside the api container:
    docker compose exec api python manage.py test dnaorder.tests.test_query_counts -v 2
"""
import re
from collections import Counter

from django.db import connection
from django.test.utils import CaptureQueriesContext

from dnaorder.models import Contact, PI, PIInstitution
from dnaorder.tests.base import (
    ApiTestCase, make_participant, make_submission, make_user,
)

#: Row counts to compare.  The difference between the two measurements divided
#: by the difference in rows is the per-row cost; fixed overhead (the count
#: query, permission lookups, each prefetch) cancels out.
FEWER_ROWS = 5
MORE_ROWS = 25

#: Queries an extra row may cost.  An endpoint that fetches its rows in bulk
#: adds none; anything at or above 1 means at least one query per row.
MAX_QUERIES_PER_ROW = 0.5


def shape(sql):
    """A query with its literals removed, so repeats of one query group together."""
    sql = re.sub(r"'[^']*'", "'?'", sql)
    sql = re.sub(r'\b\d[\d.]*\b', '?', sql)
    sql = re.sub(r'\s+', ' ', sql).strip()
    return sql


def tables(sql):
    """The tables a query reads, as a short label."""
    found = re.findall(r'(?:FROM|JOIN)\s+"([^"]+)"', sql)
    seen = list(dict.fromkeys(found))
    return ' + '.join(seen) if seen else '?'


class SubmissionQueryCountTests(ApiTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.pi_institution = PIInstitution.objects.create(name='Row Institute')
        cls.receiver = make_user('row_receiver', email='receiver@example.org')
        cls.row_participants = [
            make_user('row_participant{}'.format(n), email='participant{}@example.org'.format(n),
                      first_name='Part', last_name='Icipant{}'.format(n))
            for n in range(2)
        ]

    def setUp(self):
        super().setUp()
        self.seeded = 0
        # So a page holds exactly the rows seeded by the test.
        self.type_a.submissions.all().delete()

    def seed(self, count):
        for _ in range(count):
            n = self.seeded
            self.seeded += 1
            pi = PI.objects.create(
                email='rowpi{}@example.org'.format(n), first_name='Row', last_name='Pi{}'.format(n),
                phone='555-0100', institution=self.pi_institution,
            )
            submission = make_submission(
                self.type_a,
                first_name='Row{}'.format(n),
                # Not the fixture addresses, so these rows do not name
                # lab_a_member, submitter, pi_user or contact_user.
                email='row{}@example.org'.format(n),
                pi_email=pi.email,
                pi=pi,
                received_by=self.receiver,
            )
            Contact.objects.create(
                submission=submission, first_name='Con', last_name='Tact',
                email='rowcontact{}@example.org'.format(n),
            )
            for user in self.row_participants:
                make_participant(submission, user)

    def queries(self, url):
        """The queries one request as a member of the lab runs."""
        client = self.as_user(self.lab_a_member)
        with CaptureQueriesContext(connection) as captured:
            resp = client.get(url)
        self.assertEqual(resp.status_code, 200, url)
        return list(captured.captured_queries), resp

    def breakdown(self, queries, rows):
        """Query shapes that repeat often enough to be per-row, worst first."""
        counts = Counter(shape(q['sql']) for q in queries)
        lines = []
        for sql, count in counts.most_common():
            if count < rows / 2:
                continue
            lines.append('  {:>4} x  {:<34} {}'.format(
                count, tables(sql)[:34], sql[:150]
            ))
        return '\n'.join(lines)

    def assertFlat(self, url, check=None):
        """``url`` is requested with FEWER_ROWS seeded and again with MORE_ROWS;
        ``check(response, rows)`` can confirm the response held that many."""
        self.seed(FEWER_ROWS)
        fewer, resp = self.queries(url)
        if check:
            check(resp, FEWER_ROWS)

        self.seed(MORE_ROWS - FEWER_ROWS)
        more, resp = self.queries(url)
        if check:
            check(resp, MORE_ROWS)

        per_row = (len(more) - len(fewer)) / (MORE_ROWS - FEWER_ROWS)
        self.assertLessEqual(
            per_row, MAX_QUERIES_PER_ROW,
            '\n{} costs {:.1f} queries per row ({} queries for {} rows, {} for {}): '
            'about {:.0f} for 1000 rows and {:.0f} for 10,000.\n'
            'Repeating queries with {} rows:\n{}'.format(
                url, per_row, len(fewer), FEWER_ROWS, len(more), MORE_ROWS,
                per_row * 1000, per_row * 10000,
                MORE_ROWS, self.breakdown(more, MORE_ROWS),
            ),
        )

    def test_a_row_on_the_submissions_list_is_cheap(self):
        def check(resp, rows):
            results = resp.data['results']
            self.assertEqual(len(results), rows)
            # The rows really carry what the seeding gave them.
            row = results[0]
            self.assertEqual(row['pi']['institution']['name'], 'Row Institute')
            self.assertEqual(len(row['participants']), len(self.row_participants))
            self.assertEqual(len(row['participant_names']), len(self.row_participants))
            self.assertEqual(len(row['contacts']), 1)
            self.assertEqual(row['received_by_name'], str(self.receiver))

        self.assertFlat(
            '/api/submissions/?lab={}&page_size={}'.format(self.lab_a.lab_id, MORE_ROWS),
            check,
        )

    def test_a_row_in_the_export_is_cheap(self):
        self.assertFlat(
            '/api/submissions/export/?lab={}&export_format=csv'.format(self.lab_a.lab_id)
        )
