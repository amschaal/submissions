"""How the submissions list scales: queries per additional row.

The absolute query count for a list page is not very interesting -- it moves
whenever a prefetch is added or a filter changes.  What matters is the marginal
cost: how many queries each extra row on the page costs.  A healthy list is
flat (0 per row), because every row is served from the rows already fetched.

Measured on the expensive path on purpose: a lab member listing their own lab
(``?lab=``), where the rows neither name them nor list them as a participant,
so nothing in ``Submission.editable`` short-circuits.

On failure the message breaks the cost down by query shape, so the queries that
repeat per row can be addressed individually.

Run inside the api container:
    docker compose exec api python manage.py test dnaorder.tests.test_query_counts -v 2
"""
import re
from collections import Counter

from django.db import connection
from django.test.utils import CaptureQueriesContext

from dnaorder.tests.base import ApiTestCase, make_submission

#: Row counts to compare.  The difference between the two measurements divided
#: by the difference in rows is the per-row cost; fixed overhead (the count
#: query, permission lookups, each prefetch) cancels out.
FEWER_ROWS = 5
MORE_ROWS = 25

#: Queries an extra row may cost.  A list that fetches its rows in bulk adds
#: none; anything at or above 1 means at least one query per row.
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


class SubmissionListQueryCountTests(ApiTestCase):
    def seed(self, count):
        for index in range(count):
            make_submission(
                self.type_a,
                first_name='Row{}'.format(index),
                # Not the fixture addresses, so these rows do not name
                # lab_a_member, submitter, pi_user or contact_user.
                email='row{}@example.org'.format(index),
                pi_email='rowpi{}@example.org'.format(index),
            )

    def list_queries(self, page_size):
        """(query count, response, captured queries) for one full page."""
        client = self.as_user(self.lab_a_member)
        url = '/api/submissions/?lab={}&page_size={}'.format(
            self.lab_a.lab_id, page_size
        )
        with CaptureQueriesContext(connection) as captured:
            resp = client.get(url)
        self.assertEqual(resp.status_code, 200, resp.content)
        return len(captured), resp.data, list(captured.captured_queries)

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

    def test_a_row_on_the_submissions_list_is_cheap(self):
        # Clear the fixture's own submissions so the page holds exactly the
        # rows seeded here.
        self.type_a.submissions.all().delete()

        self.seed(FEWER_ROWS)
        fewer, data, _ = self.list_queries(FEWER_ROWS)
        self.assertEqual(len(data['results']), FEWER_ROWS)

        self.seed(MORE_ROWS - FEWER_ROWS)
        more, data, queries = self.list_queries(MORE_ROWS)
        self.assertEqual(len(data['results']), MORE_ROWS)

        per_row = (more - fewer) / (MORE_ROWS - FEWER_ROWS)
        self.assertLessEqual(
            per_row, MAX_QUERIES_PER_ROW,
            '\n{:.1f} queries per row ({} queries for {} rows, {} for {}): a page of '
            '1000 (StandardPagePagination.page_size) costs about {:.0f} and the '
            '10,000-row JSON export about {:.0f}.\n'
            'Repeating queries in the {}-row page:\n{}'.format(
                per_row, fewer, FEWER_ROWS, more, MORE_ROWS,
                per_row * 1000, per_row * 10000,
                MORE_ROWS, self.breakdown(queries, MORE_ROWS),
            ),
        )
