from jsonschema.validators import Draft6Validator
import jsonschema
import re
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
    def __init__(self, variable, value, message, skip_other_exceptions=False):
        self.variable = variable
        self.value = value
        self.message = message
        self.skip_other_exceptions = skip_other_exceptions


def get_column(variable, data=[]):
    return [line.get(variable, None) for line in data]

class BaseValidator(object):
    id = None #Must override this to something unique
    name = None #Must override
    description = None
    uses_options = True
    def __init__(self, options= {}):
        self.options = options
        if not self.id:
            raise Exception('You must define "id" for each validator')
        if not self.name:
            raise Exception('You must define "name" for each validator')
    def validate(self, variable, value, schema={}, data=[]):
        raise NotImplementedError
    def serialize(self):
        return {'id': self.id, 'name': self.name, 'description': self.description, 'uses_options': self.uses_options}

class UniqueValidator(BaseValidator):
    id = 'unique'
    name = 'Unique'
    description = 'Ensure that all values in the column are unique.'
    uses_options = False
    def validate(self, variable, value, schema={}, data=[]):
        col = get_column(variable, data)
        valid = len([val for val in col if val == value and val is not None]) < 2
        if not valid:
            raise ValidationException(variable, value, 'Value "{0}" is not unique for column "{1}"'.format(value, variable))

class RequiredValidator(BaseValidator):
    id = 'required'
    name = 'Required'
    description = 'Require that the user fill out this field.'
    uses_options = False
    def validate(self, variable, value, schema={}, data=[]):
        if value is None or value == '':
            raise ValidationException(variable, value,"This field is required.",skip_other_exceptions=True)

class RegexValidator(BaseValidator):
    id = 'regex'
    name = 'Regular Expression'
    description = 'Check input against a regular expression.'
    uses_options = True
    def __init__(self, options={}):
        super(RegexValidator, self).__init__(options)
        self.regex = self.options.get('regex',None)
        if self.regex:
            self.pattern = re.compile(self.regex)
    def validate(self, variable, value, schema={}, data=[]):
        if not self.pattern:
            return
        if not self.pattern.match(value):
            raise ValidationException(variable, value, 'Value "{0}" does not match the format: {1}'.format(value, self.regex))

class EnumValidator(BaseValidator):
    id = 'enum'
    name = 'Choices'
    description = 'Constrain input to a list of choices.'
    uses_options = True
    def validate(self, variable, value, schema={}, data=[]):
        choices = self.options.get('enum',[])
        if len(choices) == 0:
            return
        if value not in choices:
            raise ValidationException(variable, value, 'Value "{0}" is not one of the acceptable values: {1}'.format(value, ", ".join(choices)))

class NumberValidator(BaseValidator):
    id = 'number'
    name = 'Number'
    description = 'Only allow numbers, optionally within a certain range.'
    uses_options = True
    def validate(self, variable, value, schema={}, data=[]):
#         vschema = schema['properties'][variable]
        if not value and value != 0:
            return
        try:
            float(value)
        except ValueError:
            raise ValidationException(variable, value, 'Value "{0}" is not a number'.format(value))
        minimum = self.options.get('minimum', None)
        maximum = self.options.get('maximum', None)
        if minimum and maximum and (float(value) < minimum or float(value) > maximum):
            raise ValidationException(variable, value, 'Value must be in the range {1} - {2}'.format(minimum,maximum))
        if minimum and float(value) < minimum:
            raise ValidationException(variable, value, 'The minimum value is {0}'.format(minimum))
        if maximum and float(value) > maximum:
            raise ValidationException(variable, value, 'The maximum value is {0}'.format(maximum))

class FooValidator(BaseValidator):
    id = 'foo'
    name = 'Foo'
    def validate(self, variable, value, schema={}, data=[]):
        if value != 'foo':
            raise ValidationException(variable, value, 'Value must be "foo"'.format(value, variable))

VALIDATORS = [UniqueValidator, FooValidator, EnumValidator, NumberValidator, RegexValidator, RequiredValidator]
VALIDATORS_DICT = dict([(v.id, v) for v in VALIDATORS])

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
    def __init__(self, schema, data):
        self.errors = {}
        self.schema = schema
        self.data = data
    def get_validator(self, id, options={}):
        if VALIDATORS_DICT.has_key(id):
            return VALIDATORS_DICT[id](options)
    def set_error(self, index, variable, message):
        if not self.errors.has_key(index):
            self.errors[index] = {}
        if not self.errors[index].has_key(variable):
            self.errors[index][variable] = []
        self.errors[index][variable].append(message)
#     def validate_jsonschema(self):
#         v = Validator(self.schema)#Draft6Validator
#     #     print v.is_valid(data)
#         errors = {}
#         for index, row in enumerate(self.data):
#             print v.is_valid(row)
#             for error in sorted(v.iter_errors(row), key=str):
#                 if not errors.has_key(index):
#                     errors[index] = {}
#                 if error.schema_path[0] == 'properties':
#                     if not errors[index].has_key(error.schema_path[1]):
#                         errors[index][error.schema_path[1]] = []
#                     errors[index][error.schema_path[1]].append(error.message)
#                 elif error.schema_path[0] == 'required':
#                     if not errors[index].has_key(error.schema_path[1]):
#                         errors[index][error.schema_path[1]] = []
#                     errors[index][error.schema_path[1]].append('This field is required')
#                 else:
#                     print [error.message, error.path, error.absolute_path,error.schema_path,len(error.schema_path)]#. error.schema_path, error.cause]
#     #             if len(error.path) == 0:
#     #                 if not errors.has_key('all') 
#     #             print [error.message, error.path, error.absolute_path,error.schema_path,len(error.schema_path)]#. error.schema_path, error.cause]
#         return errors
    def validate(self):
#         self.errors = self.validate_jsonschema()
        for variable in self.schema['properties'].keys():
            #Add validators configured by the user
            validators = [self.get_validator(v.get('id'),v.get('options',{})) for v in self.schema['properties'][variable].get('validators', [])]
            
            #Add validators based on the JSON schema
            if variable in self.schema.get('required', []):
                validators.append(self.get_validator(RequiredValidator.id, self.schema['properties'][variable]))
            if self.schema['properties'][variable].get('unique', False):
                validators.append(self.get_validator(UniqueValidator.id, self.schema['properties'][variable]))
            if self.schema['properties'][variable].get('enum', False):
                validators.append(self.get_validator(EnumValidator.id, self.schema['properties'][variable]))
            if self.schema['properties'][variable].get('pattern', False):
                validators.append(self.get_validator(RegexValidator.id, {'regex':self.schema['properties'][variable].get('pattern')}))
            if self.schema['properties'][variable].get('type', False) == 'number':
                validators.append(self.get_validator(NumberValidator.id, self.schema['properties'][variable]))
                
            for idx, row in enumerate(self.data):
                value = row.get(variable, None)
                for validator in validators:
                    if validator:
                        try:
                            validator.validate(variable, value, self.schema, self.data)
                        except ValidationException, e:
                            self.set_error(idx, variable, e.message)
                            if e.skip_other_exceptions:
                                break
        print self.errors
        return self.errors


class SubmissionValidator(SamplesheetValidator):
#     def __init__(self, schema, data):
#         self.errors = {}
#         self.schema = schema
#         self.data = data
#     def get_validator(self, id, options={}):
#         if VALIDATORS_DICT.has_key(id):
#             return VALIDATORS_DICT[id](options)
    def set_error(self, variable, message):
#         if not self.errors.has_key(index):
#             self.errors[index] = {}
        if not self.errors.has_key(variable):
            self.errors[variable] = []
        self.errors[variable].append(message)
    def validate_jsonschema(self):
        v = Validator(self.schema)#Draft6Validator
    #     print v.is_valid(data)
        errors = {}
        v.is_valid(self.data)
        for error in sorted(v.iter_errors(self.data), key=str):
            if error.schema_path[0] == 'properties':
                if not errors.has_key(error.schema_path[1]):
                    errors[error.schema_path[1]] = []
                errors[error.schema_path[1]].append(error.message)
            elif error.schema_path[0] == 'required':
                if not errors.has_key(error.schema_path[1]):
                    errors[error.schema_path[1]] = []
                errors[error.schema_path[1]].append('This field is required')
            else:
                print [error.message, error.path, error.absolute_path,error.schema_path,len(error.schema_path)]#. error.schema_path, error.cause]
        return errors
    def validate(self):
        self.errors = self.validate_jsonschema()
        for variable in self.schema['properties'].keys():
            validators = [self.get_validator(v.get('id'),v.get('options',{})) for v in self.schema['properties'][variable].get('validators', [])]
            if self.schema['properties'][variable].get('unique', False):
                validators.append(self.get_validator(UniqueValidator.id))
            value = self.data.get(variable, None)
            for validator in validators:
                if validator:
                    try:
                        validator.validate(variable, value, self.schema, [self.data])
                    except ValidationException, e:
                        self.set_error(variable, e.message)
                        if e.skip_other_exceptions:
                            break
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
            