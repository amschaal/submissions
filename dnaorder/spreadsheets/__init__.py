from django.http import HttpResponse
from django.utils import timezone
import tablib

HEADER_TITLES = [
    "ID",
    "Internal ID",
    "Type",
    "Submitted",
    "First Name",
    "Last Name",
    "Submitter Email",
    "Submitter Phone",
    "PI First Name",
    "PI Last Name",
    "PI Email",
    "PI Phone",
    "Institute",
    "Status",
    "Status Durations",
]


def get_cols(schema, table=False):
    if table:
        return [
            v
            for v in schema.get("order", [])
            if schema["properties"][v]["type"] == "table"
        ]
    else:
        return [
            v
            for v in schema.get("order", [])
            if schema["properties"][v]["type"] != "table"
        ]


def get_headers(schema, use_title=False, table=False):
    cols = get_cols(schema, table)
    return [
        (
            schema["properties"][v].get("title")
            if use_title and "title" in schema["properties"][v]
            else v
        )
        for v in cols
    ]


def get_data(schema, data, default=None, list_delimiter=", "):
    if not data:
        return [[]]
    if isinstance(data, dict):
        data = [data]
    rows = []
    cols = get_cols(schema, table=False)
    for row in data:
        rows.append(
            [
                (
                    list_delimiter.join(row.get(v, default))
                    if isinstance(row.get(v, default), list)
                    else row.get(v, default)
                )
                for v in cols
            ]
        )
    return rows


def get_dataset(schema, data, use_titles=False):
    dataset = tablib.Dataset(headers=get_headers(schema, use_titles))
    dataset.extend(get_data(schema, data))
    return dataset


def get_submission_dataset(submission, use_titles=False):
    dataset = tablib.Dataset(headers=get_submission_headers(submission, use_titles))
    dataset.extend([get_submission_data(submission)])
    return dataset


def get_submission_headers(submission, use_title=False, custom_fields=True):
    return (
        HEADER_TITLES
        if not custom_fields
        else HEADER_TITLES + get_headers(submission.submission_schema, use_title)
    )


def get_submission_data(submission, custom_fields=True):
    data = [
        submission.id,
        submission.internal_id,
        str(submission.type),
        submission.submitted.replace(tzinfo=None),
        submission.first_name,
        submission.last_name,
        submission.email,
        submission.phone,
        submission.pi_first_name,
        submission.pi_last_name,
        submission.pi_email,
        submission.pi_phone,
        submission.institute,
        submission.status,
        submission.data.get("status_durations", {}),
    ]
    if custom_fields:
        data += get_data(submission.submission_schema, submission.submission_data)[0]
    return data


def get_custom_data(submission, headers):
    data = [submission.submission_data.get(v) for v in headers]
    return [len(d) if isinstance(d, list) else d for d in data]


def get_submissions_custom_fields(submissions):
    fields = set()
    for s in submissions:
        fields.update(s.submission_schema["order"])
        # fields.update(get_headers(s.submission_schema, table=False))
    return sorted(list(fields))


def get_submissions_dataset(submissions):
    headers = get_submissions_custom_fields(submissions)
    dataset = tablib.Dataset(headers=HEADER_TITLES + headers)
    data = [
        (get_submission_data(s, False) + get_custom_data(s, headers))
        for s in submissions
    ]
    dataset.extend(data)
    return dataset


def get_submission_table_data(submissions):
    tables = {}
    for submission in submissions:
        table_cols = get_cols(submission.submission_schema, table=True)
        # raise Exception(table_cols)
        for col in table_cols:
            if col not in tables:
                tables[col] = {"headers": set(), "data": []}
            order = set(
                submission.submission_schema.get("properties", {})
                .get(col, {})
                .get("schema", {})
                .get("order", [])
            )

            tables[col]["headers"].update(order)
            table_data = submission.submission_data.get(col)
            if isinstance(table_data, list):
                for row in table_data:
                    row["submission_id"] = submission.id
                    tables[col]["data"].append(row)
    datasets = []
    for name, table in tables.items():
        headers = ["submission_id"] + list(table["headers"])
        dataset = tablib.Dataset(headers=headers)
        dataset.title = name
        data = [[row.get(header) for header in headers] for row in table["data"]]
        dataset.extend(data)
        datasets.append(dataset)
    return datasets


def get_submissions_dataset_full_xlsx(submissions):
    submission_dataset = get_submissions_dataset(submissions)
    submission_dataset.title = "submissions"
    datasets = [submission_dataset]
    datasets += get_submission_table_data(submissions)
    databook = tablib.Databook(datasets)
    prefix = "submissions"
    format = "xlsx"
    return dataset_response(databook, prefix, format)


def dataset_response(dataset, prefix, format, timestamp=True):
    filename = (
        "{0}.{1}.{2}".format(prefix, timezone.now().strftime("%Y_%m_%d__%H_%M"), format)
        if timestamp
        else "{0}.{2}".format(prefix, format)
    )
    content_types = {
        "xls": "application/vnd.ms-excel",
        "tsv": "text/tsv",
        "csv": "text/csv",
        "json": "text/json",
        "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    }
    response_kwargs = {"content_type": content_types[format]}
    response = HttpResponse(getattr(dataset, format), **response_kwargs)
    response["Content-Disposition"] = "attachment; filename={0}".format(filename)
    return response
