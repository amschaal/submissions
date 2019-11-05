from dnaorder.validators import BaseValidator, ValidationError, ValidationWarning
from genomics.barcodes import get_all_conflicts
class BarcodeValidator(BaseValidator):
    id = 'barcode'
    name = 'Barcode Validator'
    schema = [{'variable': 'samplename', 'label': 'Samplename variable', 'type': 'text'},
              {'variable': 'pool', 'label': '(Optional) Pool variable', 'type': 'text'},
              {'variable': 'distance', 'label': 'Hamming distance', 'type': 'number'},
              ]
    def validate(self, variable, value, schema={}, data=[], row=[]):
        self.hamming_distance = int(self.options.get('distance', 2))
        self.pool = self.options.get('pool', None)
        self.sample_name = self.options.get('samplename')
        if not hasattr(self, 'errors'):
            self.validate_all(schema, data, variable)
        library = row.get(self.options.get('samplename'))
        if library and library in self.errors:
#             self.errors[library] -> {u'xyz23': [{u'distance': 0, u'xyz23': u'GTAATTGC', u'10xPN120262': u'GTAATTGC'}, {u'distance': 0, u'xyz23': u'AGTCGCTT', u'10xPN120262': u'AGTCGCTT'}, {u'distance': 0, u'xyz23': u'CACGAGAA', u'10xPN120262': u'CACGAGAA'}, {u'distance': 0, u'xyz23': u'TCGTCACG', u'10xPN120262': u'TCGTCACG'}]}
            error = 'Barcode conflicts with samples: {}.  Please ensure equal length barcodes and a hamming distance of at least {}.'.format(', '.join(self.errors[library].keys()),self.hamming_distance)
            raise ValidationWarning(variable, value, error)
    def validate_all(self, schema, data, variable):
        libraries = [{'id': d.get(self.sample_name),'pool': d.get(self.pool,''),'barcodes':d.get(variable).split(',')} for d in data if d.get(variable, None)]
        self.errors = get_all_conflicts(libraries, self.hamming_distance)
