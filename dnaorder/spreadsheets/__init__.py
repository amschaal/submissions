import tablib
def get_headers(schema, use_title=True):
    return [schema['properties'][v].get('title') if use_title and schema['properties'][v].has_key('title') else v for v in schema['order']]

def get_data(schema, data, default=None, list_delimiter=', '):
    if not data:
        return [[]]
    if isinstance(data, dict):
        data = [data]
    rows = []
    for row in data:
        rows.append([list_delimiter.join(row.get(v,default)) if isinstance(row.get(v,default), list) else row.get(v,default) for v in schema.get('order',[])])
    return rows

def get_dataset(schema, data):
    dataset = tablib.Dataset(headers=get_headers(schema))
    dataset.extend(get_data(schema, data))
    return dataset

def get_submission_dataset(submission):
    dataset = tablib.Dataset(headers=get_submission_headers(submission))
    dataset.extend(get_submission_data(submission))
    return dataset

def get_submission_headers(submission):
    return ['ID', 'Internal ID', 'Type', 'First Name', 'Last Name', 'Submitter Email', 'Submitter Phone', 'PI First Name', 'PI Last Name', 'PI Email', 'PI Phone', 'Institute'] + get_headers(submission.submission_schema)

def get_submission_data(submission):
    return [[submission.id, submission.internal_id, str(submission.type), submission.first_name, submission.last_name, submission.email, submission.phone, submission.pi_first_name, submission.pi_last_name, submission.pi_email, submission.pi_phone, submission.institute] + get_data(submission.submission_schema, submission.submission_data)[0]]