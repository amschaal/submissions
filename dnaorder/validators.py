from jsonschema.validators import Draft6Validator
import jsonschema
# Custom validators
def _required(validator, required, instance, schema):
    '''Validate 'required' properties.'''
    if not validator.is_type(instance, 'object'):
        return

    for index, requirement in enumerate(required):
        if requirement not in instance:
            error = jsonschema.ValidationError(
                '{0!r} is a required property'.format(requirement)
            )
            print '_required validator'
            print index
            error.schema_path.append(requirement)
            yield error


# Construct validator as extension of Json Schema Draft 4.
Validator = jsonschema.validators.extend(
    validator=jsonschema.validators.Draft6Validator,
    validators={
        'required': _required
    }
)

class ValidationException(Exception):
    def __init__(self, variable, value, message):
        self.variable = variable
        self.value = value
        self.message = message

def get_column(variable, data=[]):
    return [line.get(variable, None) for line in data]

def unique_validator(variable, value, schema={}, data=[]):
    col = get_column(variable, data)
    valid = len([val for val in col if val == value and val is not None]) < 2
    if not valid:
        raise ValidationException(variable, value, 'Value "{0}" is not unique for column "{1}"'.format(value, variable))

class SamplesheetValidator:
    def __init__(self, schema, data):
        self.errors = {}
        self.schema = schema
        self.data = data
    def set_error(self, index, variable, message):
        if not self.errors.has_key(index):
            self.errors[index] = {}
    def validate(self):
        for i, row in enumerate(self.data):
            for v in self.schema['properties'].keys():
                print i, v, row.get(v, None)
                try:
                    pass #validation function
                except ValidationException, e:
                    pass #do stuff

def validate_samplesheet(schema, data=[]):
    print schema
    print data
    v = Validator(schema)#Draft6Validator
    print 'valid'
#     print v.is_valid(data)
    errors = {}
    for index, row in enumerate(data):
        print v.is_valid(row)
        for error in sorted(v.iter_errors(row), key=str):
            if not errors.has_key(index):
                errors[index] = {}
            if error.schema_path[0] == 'properties':
                if not errors[index].has_key(error.schema_path[1]):
                    errors[index][error.schema_path[1]] = []
                errors[index][error.schema_path[1]].append(error.message)
            elif error.schema_path[0] == 'required':
                if not errors[index].has_key(error.schema_path[1]):
                    errors[index][error.schema_path[1]] = []
                errors[index][error.schema_path[1]].append('This field is required')
            else:
                print 'UNCAUGHT'
                print [error.message, error.path, error.absolute_path,error.schema_path,len(error.schema_path)]#. error.schema_path, error.cause]
#             if len(error.path) == 0:
#                 if not errors.has_key('all') 
#             print [error.message, error.path, error.absolute_path,error.schema_path,len(error.schema_path)]#. error.schema_path, error.cause]
    return errors
            