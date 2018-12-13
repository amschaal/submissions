import re

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
    supported_types = ['string','number','boolean']
    def __init__(self, options= {}):
        self.options = options
        if not self.id:
            raise Exception('You must define "id" for each validator')
        if not self.name:
            raise Exception('You must define "name" for each validator')
    def validate(self, variable, value, schema={}, data=[]):
        raise NotImplementedError
    def serialize(self):
        return {'id': self.id, 'name': self.name, 'description': self.description, 'uses_options': self.uses_options, 'supported_types': self.supported_types}

# Custom validators
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
    supported_types = ['string']
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
    supported_types = ['string']
    def validate(self, variable, value, schema={}, data=[]):
        choices = self.options.get('enum',[])
        if len(choices) == 0:
            return
        if isinstance(value, (list,tuple)):
            bad_values = [v for v in value if v not in choices]
            if len(bad_values) > 0:
                raise ValidationException(variable, value, 'Value(s) "{0}" not in the acceptable values: {1}'.format(", ".join(bad_values), ", ".join(choices)))
        elif value not in choices:
            raise ValidationException(variable, value, 'Value "{0}" is not one of the acceptable values: {1}'.format(value, ", ".join(choices)))

class NumberValidator(BaseValidator):
    id = 'number'
    name = 'Number'
    description = 'Only allow numbers, optionally within a certain range.'
    uses_options = True
    supported_types = ['number']
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

VALIDATORS = [UniqueValidator, EnumValidator, NumberValidator, RegexValidator, RequiredValidator]
VALIDATORS_DICT = dict([(v.id, v) for v in VALIDATORS])


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
    def validate_values(self, variable, validators):
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
    def get_validators(self, variable):
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
        return validators
    def validate(self):
#         self.errors = self.validate_jsonschema()
        for variable in self.schema['properties'].keys():
            validators = self.get_validators(variable)
            self.validate_values(variable, validators)
        print self.errors
        return self.errors

class SubmissionValidator(SamplesheetValidator):
    def set_error(self, variable, message):
        if not self.errors.has_key(variable):
            self.errors[variable] = []
        self.errors[variable].append(message)
    def validate_values(self, variable, validators):
        value = self.data.get(variable, None)
        for validator in validators:
            if validator:
                try:
                    validator.validate(variable, value, self.schema, [self.data])
                except ValidationException, e:
                    self.set_error(variable, e.message)
                    if e.skip_other_exceptions:
                        break
