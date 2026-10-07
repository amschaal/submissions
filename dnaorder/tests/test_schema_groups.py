"""Field groups in submission schemas (`groups` + `layout_order`).

`layout_order` lists ungrouped fields and group ids in display order, and each
group lists its own fields.  On save the backend rebuilds the flat `order` from
them, rejects duplicates, id collisions and malformed groups, and silently
repairs stale data left by clients that don't know about groups.
"""
import re

from dnaorder.tests.base import ApiTestCase, make_submission_type
from schema.utils import SchemaException, normalize_layout
from django.test import SimpleTestCase


def make_schema(fields=("a", "b", "c", "d"), **extra):
    schema = {
        "properties": {f: {"type": "string", "title": f.upper()} for f in fields},
        "order": list(fields),
        "required": [],
        "layout": {},
    }
    schema.update(extra)
    return schema


def group(*fields, **extra):
    return dict({"title": "Group", "fields": list(fields)}, **extra)


class NormalizeLayoutTests(SimpleTestCase):
    def test_schema_without_groups_is_unchanged(self):
        schema = make_schema(order=["d", "c", "b", "a"])
        self.assertIs(normalize_layout(schema), schema)

    def test_order_is_rebuilt_from_layout_order(self):
        schema = normalize_layout(make_schema(
            layout_order=["d", "g1", "a"],
            groups={"g1": group("c", "b")},
        ))
        self.assertEqual(schema["order"], ["d", "c", "b", "a"])
        self.assertEqual(schema["layout_order"], ["d", "g1", "a"])

    def test_input_is_not_mutated(self):
        original = make_schema(layout_order=["g1"], groups={"g1": group("a", "zz")})
        normalize_layout(original)
        self.assertEqual(original["groups"]["g1"]["fields"], ["a", "zz"])
        self.assertNotIn("b", original["layout_order"])

    def test_empty_groups_are_kept(self):
        schema = normalize_layout(make_schema(
            layout_order=["a", "empty", "b", "c", "d"],
            groups={"empty": group()},
        ))
        self.assertEqual(schema["layout_order"], ["a", "empty", "b", "c", "d"])
        self.assertEqual(schema["order"], ["a", "b", "c", "d"])

    def test_stale_ids_are_dropped(self):
        # "zz" was deleted by a client that doesn't know about groups
        schema = normalize_layout(make_schema(
            layout_order=["zz", "g1", "missing_group"],
            groups={"g1": group("a", "zz", "b", "c", "d")},
        ))
        self.assertEqual(schema["layout_order"], ["g1"])
        self.assertEqual(schema["groups"]["g1"]["fields"], ["a", "b", "c", "d"])

    def test_unplaced_fields_and_groups_are_appended(self):
        # "c" and "d" were added by a client that doesn't know about groups,
        # "e" is in properties but missing from order too
        base = make_schema(fields=("a", "b", "c", "d", "e"))
        base["order"] = ["a", "b", "d", "c"]
        base.update(layout_order=["b", "g1"], groups={"g1": group("a"), "g2": group()})
        schema = normalize_layout(base)
        self.assertEqual(schema["layout_order"], ["b", "g1", "d", "c", "e", "g2"])
        self.assertEqual(schema["order"], ["b", "a", "d", "c", "e"])

    def test_layout_order_alone_is_normalized(self):
        schema = normalize_layout(make_schema(layout_order=["c"]))
        self.assertEqual(schema["layout_order"], ["c", "a", "b", "d"])
        self.assertEqual(schema["order"], ["c", "a", "b", "d"])
        self.assertEqual(schema["groups"], {})

    def assertInvalid(self, schema, message):
        with self.assertRaisesRegex(SchemaException, re.escape(message)):
            normalize_layout(schema)

    def test_field_in_two_groups_is_rejected(self):
        self.assertInvalid(make_schema(
            layout_order=["g1", "g2"], groups={"g1": group("a"), "g2": group("a")},
        ), '"a" appears more than once')

    def test_field_both_ungrouped_and_grouped_is_rejected(self):
        self.assertInvalid(make_schema(
            layout_order=["a", "g1"], groups={"g1": group("a")},
        ), '"a" appears more than once')

    def test_duplicate_in_layout_order_is_rejected(self):
        self.assertInvalid(make_schema(layout_order=["a", "b", "a"]), '"a" appears more than once')

    def test_group_id_colliding_with_field_is_rejected(self):
        self.assertInvalid(make_schema(
            layout_order=["a"], groups={"a": group("b")},
        ), 'Group id "a" is also a field name')

    def test_nested_groups_are_rejected(self):
        self.assertInvalid(make_schema(
            layout_order=["g1"], groups={"g1": group("g2"), "g2": group("a")},
        ), 'cannot contain group "g2"')

    def test_malformed_groups_are_rejected(self):
        self.assertInvalid(make_schema(groups=[]), '"groups" must be an object')
        self.assertInvalid(make_schema(layout_order={}), '"layout_order" must be a list')
        self.assertInvalid(make_schema(groups={"g1": "x"}), 'must be an object')
        self.assertInvalid(make_schema(groups={"g1": {"fields": []}}), 'requires a title')
        self.assertInvalid(make_schema(groups={"g1": group(title=" ")}), 'requires a title')
        self.assertInvalid(make_schema(groups={"g1": dict(group(), fields="a")}), 'must be a list')
        self.assertInvalid(make_schema(groups={"g1": group(display="tabs")}), 'display must be one of')


class SubmissionTypeSchemaGroupsApiTests(ApiTestCase):
    def url(self, submission_type):
        return "/api/submission_types/{}/".format(submission_type.id)

    def patch_schema(self, submission_type, schema):
        return self.as_user(self.lab_a_member).patch(
            self.url(submission_type), {"submission_schema": schema}, format="json"
        )

    def test_save_normalizes_order(self):
        submission_type = make_submission_type(self.lab_a, name="Grouped")
        resp = self.patch_schema(submission_type, make_schema(
            layout_order=["d", "g1"],
            groups={"g1": group("b", "a", display="header", collapsible=True,
                                layout={"width": "col-md-6"}, printing={"label": "G"})},
        ))
        self.assertEqual(resp.status_code, 200, resp.content)
        submission_type.refresh_from_db()
        schema = submission_type.submission_schema
        self.assertEqual(schema["order"], ["d", "b", "a", "c"])
        self.assertEqual(schema["layout_order"], ["d", "g1", "c"])
        # Group options are stored as sent
        self.assertEqual(schema["groups"]["g1"]["layout"], {"width": "col-md-6"})
        self.assertTrue(schema["groups"]["g1"]["collapsible"])

    def test_invalid_groups_are_rejected(self):
        submission_type = make_submission_type(self.lab_a, name="Grouped")
        before = submission_type.submission_schema
        resp = self.patch_schema(submission_type, make_schema(
            layout_order=["g1", "g2"], groups={"g1": group("a"), "g2": group("a")},
        ))
        self.assertEqual(resp.status_code, 400, resp.content)
        self.assertIn("submission_schema", resp.data)
        submission_type.refresh_from_db()
        self.assertEqual(submission_type.submission_schema, before)

    def test_schema_without_groups_is_saved_as_is(self):
        submission_type = make_submission_type(self.lab_a, name="Plain")
        schema = make_schema(order=["d", "c", "b", "a"])
        resp = self.patch_schema(submission_type, schema)
        self.assertEqual(resp.status_code, 200, resp.content)
        submission_type.refresh_from_db()
        self.assertEqual(submission_type.submission_schema, schema)
