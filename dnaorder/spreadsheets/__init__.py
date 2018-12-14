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