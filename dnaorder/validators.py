import re

"""
    ValidationException validates a single value
"""
from dnaorder.models import Term, Vocabulary
class ValidationException(Exception):
    def __init__(self, variable, value, message, skip_other_exceptions=False):
        self.variable = variable
        self.value = value
        self.message = message
        self.skip_other_exceptions = skip_other_exceptions

class MultiValidationException(Exception):
    def __init__(self, exceptions, skip_other_exceptions=False):
        self.exceptions = exceptions
        self.skip_other_exceptions = skip_other_exceptions

class TableValidationException(Exception):
    def __init__(self, errors, warnings, skip_other_exceptions=False):
        self.errors = errors if len(errors) else None
        self.warnings = warnings if len(warnings) else None
        self.skip_other_exceptions = skip_other_exceptions

class ValidationError(ValidationException):
    pass

class ValidationWarning(ValidationException):
    pass


def get_column(variable, data=[]):
    return [line.get(variable, None) for line in data]

class BaseValidator(object):
    id = None #Must override this to something unique
    name = None #Must override
    description = None
    uses_options = True
    schema = None
    supported_types = ['string','number','boolean']
    def __init__(self, validator, options={}):
        self.validator = validator
        self.options = options
        self.validation_class = ValidationWarning if self.options.get('warning') else ValidationError
        if not self.id:
            raise Exception('You must define "id" for each validator')
        if not self.name:
            raise Exception('You must define "name" for each validator')
    def validate(self, variable, value, schema={}, data=[], row=[]):
        raise NotImplementedError
    def validate_all(self, variable, schema={}, data=[]):
        exceptions = {}
        for idx, row in enumerate(data):
            value = row.get(variable, None)
            try:
                self.validate(variable, value, schema, data, row)
            except ValidationException as e:
                if not idx in exceptions:
                    exceptions[idx] = []
                exceptions[idx].append(e)
        if len(exceptions) > 0:
            raise MultiValidationException(exceptions)
        # @todo: return cleaned data
    @classmethod
    def serialize(cls):
        return {'id': cls.id, 'name': cls.name, 'description': cls.description, 'uses_options': cls.uses_options, 'schema': cls.schema, 'supported_types': cls.supported_types}

class TermValidator(BaseValidator):
    id = 'term'
    name = 'Vocabulary Term'
    description = 'Validate agains a controlled vocabulary'
    uses_options = True
    schema = [{'variable': 'vocab', 'label': 'Vocabulary', 'type': 'text', 'enum': Vocabulary.objects.values_list('id', flat=True)},
              ]
    supported_types = ['string']
    def __init__(self, validator, options={}):
        self.validator = validator
        super(TermValidator, self).__init__(validator, options)
        self.vocab = self.options.get('vocab',None)
    def validate(self, variable, value, schema={}, data=[], row=[]):
        if not hasattr(self, 'vocab'):
            return
        if not Term.objects.filter(vocabulary=self.vocab, value=value).exists():
            raise self.validation_class(variable, value, 'Value "{0}" does not match any terms in the vocabulary: {1}'.format(value, self.vocab))

class VocabularyValidator(BaseValidator):
    id = 'vocab'
    name = 'Validate Vocabulary Database Selection'
    description = 'Validate that the user chose a valid vocabulary database'
    supported_types = ['string']
    uses_options = False
    def __init__(self, validator, options={}):
        self.validator = validator
        super(VocabularyValidator, self).__init__(validator, options)
        if not hasattr(VocabularyValidator,'vocabularies'):
            VocabularyValidator.vocabularies = Vocabulary.objects.values_list('id', flat=True)
    def validate(self, variable, value, schema={}, data=[], row=[]):
        if value not in VocabularyValidator.vocabularies:
            raise self.validation_class(variable, value, '"{0}" is not a valid selection'.format(value))



class TableValidator(BaseValidator):
    id = 'table'
    name = 'Table'
    description = 'Validate a table based on a schema.'
    uses_options = False
    supported_types = []
    def validate_all(self, variable, schema={}, data=[]):
        for idx, d in enumerate(data):
            table = d.get(variable, None)
            if table:
                validator = SamplesheetValidator(self.options.get('schema'), table)
                errors, warnings = validator.validate()

# Custom validators
class UniqueValidator(BaseValidator):
    id = 'unique'
    name = 'Unique'
    description = 'Ensure that all values in the column are unique.'
    uses_options = False
    def validate(self, variable, value, schema={}, data=[], row=[]):
        col = get_column(variable, data)
        valid = len([val for val in col if val == value and val is not None]) < 2
        if not valid:
            raise self.validation_class(variable, value, 'Value "{0}" is not unique for column "{1}"'.format(value, variable))

class RequiredValidator(BaseValidator):
    id = 'required'
    name = 'Required'
    description = 'Require that the user fill out this field. Internal fields are not required.'
    uses_options = False
    def validate(self, variable, value, schema={}, data=[], row=[]):
        if schema['properties'].get(variable,{}).get('internal', False):
            return
        if value is None or value == '':
            raise self.validation_class(variable, value,"This field is required.",skip_other_exceptions=True)

class RegexValidator(BaseValidator):
    id = 'regex'
    name = 'Regular Expression'
    description = 'Check input against a regular expression.'
    uses_options = True
    schema = [{'variable': 'regex', 'label': 'Regex', 'type': 'text'}]
    supported_types = ['string']
    def __init__(self, validator, options={}):
        self.validator = validator
        super(RegexValidator, self).__init__(validator, options)
        self.regex = self.options.get('regex',None)
        if self.regex:
            self.pattern = re.compile(self.regex)
    def validate(self, variable, value, schema={}, data=[], row=[]):
        if not hasattr(self, 'pattern'):
            return
        if not self.pattern.match(str(value)):
            raise self.validation_class(variable, value, 'Value "{0}" does not match the format: {1}'.format(value, self.regex))

class FKValidator(BaseValidator):
    id = 'fk'
    name = 'Foreign Key Validator'
    description = 'Foreign Key Validator'
    uses_options = False
    supported_types = []
    def __init__(self, validator, options={}):
        self.validator = validator
        super(FKValidator, self).__init__(validator, options)
        self.fk = self.options.get('fk', [])
        if len(self.fk) == 2 and self.validator.root:
            self.table, self.column = self.fk
            self.ref_table = self.validator.root.data.get(self.table, [])
            self.ref_column = [row.get(self.column, None) for row in self.ref_table]
    def validate(self, variable, value, schema={}, data=[], row=[]):
        if hasattr(self, 'ref_column') and value and value != '':
            count = self.ref_column.count(value)
            if count == 0:
                raise self.validation_class(variable, value, 'Value "{0}" is not found in table: {1}, column: {2}'.format(value, self.table, self.column))
            if count > 1:
                raise self.validation_class(variable, value, 'Value "{0}" has multiple entries in referenced table: {1}, column: {2}'.format(value, self.table, self.column))

class EnumValidator(BaseValidator):
    id = 'enum'
    name = 'Choices'
    description = 'Do not use this validator for the time being.  Please enter choices under main validation menu.'
    uses_options = True
    supported_types = ['string']
    schema = [{'variable': 'enum', 'label': 'Choices', 'type': 'text'}]
    def validate_all(self, variable, schema={}, data=[]):
        self.multiple = schema['properties'][variable].get('multiple', False)
        BaseValidator.validate_all(self, variable, schema=schema, data=data)
    def validate(self, variable, value, schema={}, data=[], row=[]):
        if not value:
            return
        choices = self.options.get('enum',[])
        if len(choices) == 0:
            return
        if self.multiple and isinstance(value, str):
            value = value.split(',')
        if isinstance(value, (list,tuple)):
            bad_values = [v for v in value if v.strip() not in choices]
            if len(bad_values) > 0:
                raise self.validation_class(variable, value, 'Value(s) "{0}" not in the acceptable values: {1}'.format(", ".join(bad_values), ", ".join(choices)))
        elif value not in choices:
            raise self.validation_class(variable, value, 'Value "{0}" is not one of the acceptable values: {1}'.format(value, ", ".join(choices)))

class NumberValidator(BaseValidator):
    id = 'number'
    name = 'Number'
    description = 'Only allow numbers, optionally within a certain range.'
    uses_options = True
    supported_types = ['number']
    schema = [{'variable': 'minimum', 'label': 'Minimum', 'type': 'number'}, {'variable': 'maximum', 'label': 'Maximum', 'type': 'number'}]
    def validate(self, variable, value, schema={}, data=[], row=[]):
#         vschema = schema['properties'][variable]
        if not value and value != 0:
            return
        try:
            float(value)
        except ValueError:
            raise self.validation_class(variable, value, 'Value "{0}" is not a number'.format(value))
        
        maximum = self.options.get('maximum', None)
        try:
            minimum = float(self.options.get('minimum'))
        except:
            minimum = None
        try:
            maximum = float(self.options.get('maximum'))
        except:
            maximum = None
        if minimum and maximum and (float(value) < minimum or float(value) > maximum):
            raise self.validation_class(variable, value, 'Value must be in the range {0} - {1}'.format(minimum,maximum))
        if minimum and float(value) < minimum:
            raise self.validation_class(variable, value, 'The minimum value is {0}'.format(minimum))
        if maximum and float(value) > maximum:
            raise self.validation_class(variable, value, 'The maximum value is {0}'.format(maximum))

class AdapterValidator(BaseValidator):
    id = 'adapter'
    name = 'Adapter Validator'
    schema = [{'variable': 'samplename', 'label': 'Samplename variable', 'type': 'text'},
              {'variable': 'db', 'label': 'Database variable', 'type': 'text'},
              {'variable': 'adapter', 'label': 'Adapter variable', 'type': 'text'}
              ]
    def validate(self, variable, value, schema={}, data=[], row=[]):
        if not hasattr(self, 'errors'):
            self._validate_all(schema, data)
        library = row.get(self.options.get('samplename'))
        if library and library in self.errors:
#             self.errors[library] -> {u'xyz23': [{u'distance': 0, u'xyz23': u'GTAATTGC', u'10xPN120262': u'GTAATTGC'}, {u'distance': 0, u'xyz23': u'AGTCGCTT', u'10xPN120262': u'AGTCGCTT'}, {u'distance': 0, u'xyz23': u'CACGAGAA', u'10xPN120262': u'CACGAGAA'}, {u'distance': 0, u'xyz23': u'TCGTCACG', u'10xPN120262': u'TCGTCACG'}]}
            error = 'Barcode conflicts with samples: {}'.format(', '.join(self.errors[library].keys()))
            raise self.validation_class(variable, value, error)
    def _validate_all(self, schema, data):
        import json
        import urllib
        libraries = [{'id': d.get(self.options.get('samplename')),'adapter_db':d.get(self.options.get('db')),'adapter':d.get(self.options.get('adapter'))} for d in data]
        data = {
                'libraries': libraries
        }
        data = json.dumps(data).encode("utf-8")
        req = urllib.request.Request('http://sims.ucdavis.edu:8000/api/libraries/check_adapters/')
        req.add_header('Content-Type', 'application/json')
        try:
            response = urllib.request.urlopen(req, data=data)
            self.errors = json.loads(response.read()).get('conflicts',{})
        except Exception as e:
            self.errors = {}

class FooValidator(BaseValidator):
    id = 'foo'
    name = 'Foo'
    def validate(self, variable, value, schema={}, data=[], row=[]):
        if value != 'foo':
            raise self.validation_class(variable, value, 'Value must be "foo"'.format(value, variable))

def get_validators():
    from genomics.validators import BarcodeValidator
    return [FKValidator, UniqueValidator, EnumValidator, NumberValidator, RegexValidator, RequiredValidator, TermValidator, VocabularyValidator, BarcodeValidator]

VALIDATORS = get_validators()
VALIDATORS_DICT = dict([(v.id, v) for v in VALIDATORS])


class SamplesheetValidator: #TableValidator (List of Objects)
    def __init__(self, schema, data, clear_empty_rows=True, parent=None):
        self.errors = {}
        self.warnings = {}
        self.schema = schema
        self.data = data
        self.parent = parent
        if clear_empty_rows:
            self.clear_empty_rows()
    @property
    def root(self):
        root = self.parent
        while root and getattr(root, 'parent', None):
            root = root.parent
        return root
    def clear_empty_rows(self):
        while True:
            if len(self.data) > 1 and self.row_is_empty(self.data[-1]):
                self.data.pop()
            else:
                return
    def row_is_empty(self, row):
        for variable in self.schema['properties'].keys():
            if row.get(variable, ''):
                return False
        return True
    def get_validator(self, id, options={}):
        if id in VALIDATORS_DICT:
            return VALIDATORS_DICT[id](self, options)
    def set_error(self, index, variable, error):
        if not index in self.errors:
            self.errors[index] = {}
        if not variable in self.errors[index]:
            self.errors[index][variable] = []
        self.errors[index][variable].append(error)
    def set_warning(self, index, variable, warning):
        if not index in self.warnings:
            self.warnings[index] = {}
        if not variable in self.warnings[index]:
            self.warnings[index][variable] = []
        self.warnings[index][variable].append(warning)
    def validate_values(self, variable, validators):
        for idx, row in enumerate(self.data):
            value = row.get(variable, None)
            for validator in validators:
                if validator:
                    try:
                        validator.validate(variable, value, self.schema, self.data, row)
                    except ValidationWarning as e:
                        self.set_warning(idx, e.variable, e.message)
                        if e.skip_other_exceptions:
                            break
                    except ValidationError as e:
                        self.set_error(idx, e.variable, e.message)
                        if e.skip_other_exceptions:
                            break
    def validate_all(self, variable, validators):
        data = self.data if isinstance(self.data, list) else [self.data]
        if self.schema['properties'][variable].get('type', False) == 'table':
            schema = self.schema['properties'][variable].get('schema')
            for idx, d in enumerate(data):
                table = d.get(variable, None)
                if table:
                    validator = SamplesheetValidator(schema, table, parent=self)
                    errors, warnings = validator.validate()
                    if len(errors):
                        self.set_error(idx, variable, errors)
                    if len(warnings):
                        self.set_warning(idx, variable, warnings)
        for validator in validators:
            if validator:
                try:
                    validator.validate_all(variable, self.schema, data)
                except MultiValidationException as e:
                    for idx, exceptions in e.exceptions.items():
                        for exception in exceptions:
                            if isinstance(exception, ValidationError):
                                self.set_error(idx, exception.variable, exception.message)
                            elif isinstance(exception, ValidationWarning):
                                self.set_warning(idx, exception.variable, exception.message)
    def get_validators(self, variable):
        #Add validators configured by the user
        validators = [self.get_validator(v.get('id'),v.get('options',{})) for v in self.schema['properties'][variable].get('validators', [])]
        #Add validators based on the JSON schema
        if self.schema['properties'][variable].get('fk', False):
            validators.append(self.get_validator(FKValidator.id, self.schema['properties'][variable]))
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
        for variable in self.schema['properties'].keys():
            validators = self.get_validators(variable)
            self.validate_all(variable, validators)
        return (self.errors, self.warnings)
    def cleaned(self):
        # Right now just filters out fields not in schema properties.  Should eventually add clean method to validator so validators can actually modify values.
        cleaned = []
        for idx, row in enumerate(self.data):
            cleaned.append(dict([(variable,row.get(variable, None))  for variable in (list(self.schema['properties'].keys())+['id'])]))
        return cleaned

class SubmissionValidator(SamplesheetValidator): #Object validator
    def __init__(self, schema, data):
        super(SubmissionValidator, self).__init__(schema, data, clear_empty_rows=False)
    def set_error(self, index, variable, message):
        if not variable in self.errors:
            self.errors[variable] = []
        self.errors[variable].append(message)
    def set_warning(self, index, variable, message):
        if not variable in self.warnings:
            self.warnings[variable] = []
        self.warnings[variable].append(message)
    def validate_values(self, variable, validators):
        value = self.data.get(variable, None)
        for validator in validators:
            if validator:
                try:
                    validator.validate(variable, value, self.schema, [self.data], [self.data])
                except ValidationWarning as e:
                    self.set_warning(e.variable, e.message)
                    if e.skip_other_exceptions:
                        break
                except ValidationError as e:
                    self.set_error(e.variable, e.message)
                    if e.skip_other_exceptions:
                        break
                except TableValidationException as e:
                    if e.errors:
                        self.set_error(variable, e.errors)
                    if e.warnings:
                        self.set_warning(variable, e.warnings)
    def cleaned(self):
        # Right now just filters out fields not in schema properties.  Should eventually add clean method to validator so validators can actually modify values.
        return dict([(variable,self.data.get(variable, None))  for variable in self.schema['properties'].keys()])
