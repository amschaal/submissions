from builtins import property

class SchemaException(Exception):
    pass

class Schema(object):
    TYPE_TABLE = 'table'
    TYPE_TEXT = 'text'
    TYPE_NUMBER = 'number'
    TYPE_BOOLEAN = 'boolean'
    def __init__(self, schema, data=[]):
        self.schema = schema
        self.data = data
    def get_variables_of_type(self, TYPE):
        try:
            return [v for v in self.schema['order'] if self.schema['properties'][v]['type'] == TYPE]
        except:
            raise SchemaException('Poorly formed schema')
    @property
    def table_variables(self):
        return self.get_variables_of_type(Schema.TYPE_TABLE)
    def variable_title(self, variable):
        title =self.schema['properties'][variable].get('title', None)
        return title if title is not None else variable

def schema_to_filters(schema):
    filters = {}
    for v, definition in schema['properties'].items():
        if definition['type'] == 'table' and 'schema' in definition:
            table, table_definition = v, definition
            for v, definition in table_definition['schema']['properties'].items():
                v = '{}__{}'.format(table, v)
                if definition['type'] == 'string':
                    filters[v] = {'variable': v, 'type': definition['type'], 'title': definition.get('title',v), 'filters': [{'label':'=', 'filter': 'submission_data__{}__contains'.format(v)}]}
                    if definition.get('enum'):
                        filters[v]['enum'] = definition.get('enum')
                elif definition['type'] == 'number':
                    filters[v] = {'variable': v, 'type': definition['type'], 'title': definition.get('title',v), 'filters': [{'label':'=', 'filter': 'submission_data__{}__contains'.format(v)}]}
        elif definition['type'] == 'string':
            filters[v] = {'variable': v, 'type': definition['type'], 'title': definition.get('title',v), 'filters': [{'label':'=', 'filter': 'submission_data__{}'.format(v)}, {'label': 'contains', 'filter': 'submission_data__{}__icontains'.format(v)}]}
            if definition.get('enum'):
                filters[v]['enum'] = definition.get('enum')
        elif definition['type'] == 'number':
            filters[v] = {'variable': v, 'type': definition['type'], 'title': definition.get('title',v), 'filters': [{'label':'=', 'filter': 'submission_data__{}'.format(v)}, {'label': '>', 'filter': 'submission_data__{}__gt'.format(v)}, {'label': '<', 'filter': 'submission_data__{}__lt'.format(v)}]}
    return filters

def submission_type_schema_filters(submission_type):
    return schema_to_filters(submission_type.submission_schema)

def all_submission_type_filters(lab):
    filters = []
    filters.append({'name': 'ALL', 'id': 'ALL', 'filters': schema_to_filters(lab.submission_variables)})
    for t in lab.submission_types.all():
        type_filters = submission_type_schema_filters(t)
        filters.append({'name': t.name, 'id': t.id, 'filters': type_filters})
    return filters