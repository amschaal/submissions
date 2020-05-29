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