from dnaorder.validators import BaseValidator, ValidationError, ValidationWarning,\
    MultiValidationException
from genomics.barcodes import get_all_conflicts
class BarcodeValidator(BaseValidator):
    id = 'barcode'
    name = 'Barcode Validator'
    schema = [{'variable': 'samplename', 'label': 'Samplename variable', 'type': 'text'},
              {'variable': 'barcode2', 'label': '(Optional) Second barcode variable for dual barcodes', 'type': 'text'},
              {'variable': 'pool', 'label': '(Optional) Pool variable', 'type': 'text'},
              {'variable': 'distance', 'label': 'Hamming distance (default 1)', 'type': 'number'},
              ]
    def validate(self, variable, value, schema={}, data=[], row=[]):
        self.hamming_distance = int(self.options.get('distance', 1))
        self.pool = self.options.get('pool', None)
        self.sample_name = self.options.get('samplename')
        self.barcode2 = self.options.get('barcode2', None)
        if not hasattr(self, 'errors'):
            self._validate_all(schema, data, variable)
        library = row.get(self.options.get('samplename'))
        if library and library in self.errors:
#             self.errors[library] -> {u'xyz23': [{u'distance': 0, u'xyz23': u'GTAATTGC', u'10xPN120262': u'GTAATTGC'}, {u'distance': 0, u'xyz23': u'AGTCGCTT', u'10xPN120262': u'AGTCGCTT'}, {u'distance': 0, u'xyz23': u'CACGAGAA', u'10xPN120262': u'CACGAGAA'}, {u'distance': 0, u'xyz23': u'TCGTCACG', u'10xPN120262': u'TCGTCACG'}]}
            error = 'Barcode conflicts with samples: {}.  Please ensure equal length barcodes and a hamming distance of at least {}.'.format(', '.join(self.errors[library].keys()),self.hamming_distance)
            raise ValidationWarning(variable, value, error)
    def _validate_all(self, schema, data, variable):
        libraries = []
        for idx, d in enumerate(data):
            if d.get(variable, None):
                barcodes = {variable:d.get(variable).split(',')}
                if self.barcode2 and d.get(self.barcode2, False):
                    barcodes[self.barcode2] = d.get(self.barcode2).split(',')
                libraries.append({'id': idx,'pool': d.get(self.pool,''),'barcodes': barcodes, 'row': idx}) #d.get(self.sample_name)
#         libraries = [{'id': d.get(self.sample_name),'pool': d.get(self.pool,''),'barcodes': {variable:d.get(variable).split(','), self.barcode2:d.get(self.barcode2).split(',')} } for d in data if d.get(variable, None)]
        self.errors = get_all_conflicts(libraries, self.hamming_distance)
    def validate_all(self, variable, schema={}, data=[]):
        self.hamming_distance = int(self.options.get('distance', 1))
        self.pool = self.options.get('pool', None)
        self.sample_name = self.options.get('samplename')
        self.barcode2 = self.options.get('barcode2', None)
        libraries = []
        for idx, d in enumerate(data):
            if d.get(variable, None):
                barcodes = {variable:d.get(variable).split(',')}
                if self.barcode2 and d.get(self.barcode2, False):
                    barcodes[self.barcode2] = d.get(self.barcode2).split(',')
                libraries.append({'id': idx,'pool': d.get(self.pool,''),'barcodes': barcodes })
#         libraries = [{'id': d.get(self.sample_name),'pool': d.get(self.pool,''),'barcodes': {variable:d.get(variable).split(','), self.barcode2:d.get(self.barcode2).split(',')} } for d in data if d.get(variable, None)]
        
        self.errors = get_all_conflicts(libraries, self.hamming_distance)
        print("ERRORS!!!!!!",self.errors)
        exceptions = {}
        for idx, row in enumerate(data):
            if idx in self.errors:
                if not idx in exceptions:
                    exceptions[idx] = []
                warning = 'Barcode conflicts with sample rows: {}.  Please ensure equal length barcodes and a hamming distance of at least {}.'.format(', '.join([str(i+1) for i in self.errors[idx].keys()]),self.hamming_distance)
                exceptions[idx].append(ValidationWarning(variable, None, warning))
                if self.barcode2:
                    exceptions[idx].append(ValidationWarning(self.barcode2, None, warning))
        if len(exceptions) > 0:
            raise MultiValidationException(exceptions)