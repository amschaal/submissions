import tablib
def get_headers(schema, use_title=True):
    return [schema['properties'][v].get('title') if use_title and schema['properties'][v].has_key('title') else v for v in schema['order']]

def get_data(schema, data, default=None, list_delimiter=', '):
    if not data:
        return []
    if isinstance(data, dict):
        data = [data]
#     print schema
#     print data
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
    return ['ID', 'Internal ID', 'Type', 'Submitter', 'Submitter Email', 'Submitter Phone', 'PI', 'PI Email', 'Institute'] + get_headers(submission.type.schema)

def get_submission_data(submission):
    return [[submission.id, submission.internal_id, str(submission.type), submission.name, submission.email, submission.phone, submission.pi_name, submission.pi_email, submission.institute] + get_data(submission.type.schema, submission.submission_data)[0]]