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

class BaseValidator:
    id = None #Must override this to something unique
    name = None #Must override
    description = None
    def __init__(self, options= {}):
        self.options = options
        if not self.id:
            raise Exception('You must define "id" for each validator')
        if not self.name:
            raise Exception('You must define "name" for each validator')
    def validate(self, variable, value, schema={}, data=[]):
        raise NotImplementedError

class UniqueValidator(BaseValidator):
    id = 'unique'
    name = 'Unique'
    def validate(self, variable, value, schema={}, data=[]):
        col = get_column(variable, data)
        valid = len([val for val in col if val == value and val is not None]) < 2
        if not valid:
            raise ValidationException(variable, value, 'Value "{0}" is not unique for column "{1}"'.format(value, variable))

class FooValidator(BaseValidator):
    id = 'foo'
    name = 'Foo'
    def validate(self, variable, value, schema={}, data=[]):
        if value != 'foo':
            raise ValidationException(variable, value, 'Value must be "foo"'.format(value, variable))

VALIDATORS = [UniqueValidator, FooValidator]


def unique_validator(variable, value, schema={}, data=[]): #make this a class?
    col = get_column(variable, data)
    valid = len([val for val in col if val == value and val is not None]) < 2
    if not valid:
        raise ValidationException(variable, value, 'Value "{0}" is not unique for column "{1}"'.format(value, variable))

def get_validator(id, options):
    #This is for testing.  This will be configurable.  Also, validators may be cached, etc.
    if id == 'unique':
        return unique_validator

class SamplesheetValidator:
    validators = dict([(v.id, v) for v in VALIDATORS])
    def __init__(self, schema, data):
        self.errors = {}
        self.schema = schema
        self.data = data
    def get_validator(self, id, options):
        if self.validators.has_key(id):
            return self.validators[id](options)
    def set_error(self, index, variable, message):
        if not self.errors.has_key(index):
            self.errors[index] = {}
        if not self.errors[index].has_key(variable):
            self.errors[index][variable] = []
        self.errors[index][variable].append(message)
    def validate_jsonschema(self):
        v = Validator(self.schema)#Draft6Validator
    #     print v.is_valid(data)
        errors = {}
        for index, row in enumerate(self.data):
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
                    print [error.message, error.path, error.absolute_path,error.schema_path,len(error.schema_path)]#. error.schema_path, error.cause]
    #             if len(error.path) == 0:
    #                 if not errors.has_key('all') 
    #             print [error.message, error.path, error.absolute_path,error.schema_path,len(error.schema_path)]#. error.schema_path, error.cause]
        return errors
    def validate(self):
        self.errors = self.validate_jsonschema()
        for variable in self.schema['properties'].keys():
            validators = [self.get_validator(v.get('id'),v.get('options',{})) for v in self.schema['properties'][variable].get('validators', [])]
#             if self.schema['properties'][variable].get('unique', False):
#                 validators.append(unique_validator)
            for idx, row in enumerate(self.data):
                value = row.get(variable, None)
                for validator in validators:
                    if validator:
                        try:
                            validator.validate(variable, value, self.schema, self.data)
                        except ValidationException, e:
                            self.set_error(idx, variable, e.message)
        return self.errors

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
            