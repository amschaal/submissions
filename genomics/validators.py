from dnaorder.validators import BaseValidator, ValidationError, ValidationWarning,\
    MultiValidationException
from genomics.barcodes import get_all_conflicts
import re

class BarcodeValidator(BaseValidator):
    regex = re.compile('^[ATGCN,]*$')
    id = 'barcode'
    name = 'Barcode Validator'
    schema = [{'variable': 'samplename', 'label': 'Samplename variable', 'type': 'text'},
              {'variable': 'barcode2', 'label': '(Optional) Second barcode variable for dual barcodes', 'type': 'text'},
              {'variable': 'pool', 'label': '(Optional) Pool variable', 'type': 'text'},
              {'variable': 'distance', 'label': 'Hamming distance (default 1)', 'type': 'number'},
              ]
    def validate_all(self, variable, schema={}, data=[]):
        hamming_distance = int(self.options.get('distance', 1))
        pool = self.options.get('pool', None)
        sample_name = self.options.get('samplename')
        barcode2 = self.options.get('barcode2', None)
        libraries = []
        for idx, d in enumerate(data):
            if d.get(variable, None):
                barcodes = {variable:d.get(variable).split(',')}
                if barcode2 and d.get(barcode2, False):
                    barcodes[barcode2] = d.get(barcode2).split(',')
                libraries.append({'id': idx,'pool': d.get(pool,''),'barcodes': barcodes })
        
        errors = get_all_conflicts(libraries, hamming_distance)
        
        exceptions = {}
        for idx, d in enumerate(data):
            #First check to make sure regex matches
            b1 = d.get(variable, '')
            if not BarcodeValidator.regex.match(b1):
                if not idx in exceptions:
                    exceptions[idx] = []
                exceptions[idx].append(ValidationError(variable, None, 'Barcodes should only contain a,t,g,c,n'))
            b2 = d.get(barcode2, '')
            if barcode2 and not BarcodeValidator.regex.match(b2):
                if not idx in exceptions:
                    exceptions[idx] = []
                exceptions[idx].append(ValidationError(barcode2, None, 'Barcodes should only contain a,t,g,c,n'))

            #Now go through barcode conflicts
            if idx in errors:
                if not idx in exceptions:
                    exceptions[idx] = []
                warning = 'Barcode conflicts with sample rows: {}.  Please ensure equal length barcodes and a hamming distance of at least {}.'.format(', '.join([str(i+1) for i in errors[idx].keys()]),hamming_distance)
                exceptions[idx].append(ValidationWarning(variable, None, warning))
                if barcode2:
                    exceptions[idx].append(ValidationWarning(barcode2, None, warning))
        if len(exceptions) > 0:
            raise MultiValidationException(exceptions)