from __builtin__ import file
import tablib
from django.utils.functional import cached_property

class SampleSheet(object):
    _SAMPLE_ID = '*sample_name'
    def __init__(self,file,header_index=0,data_index=None,start_column=None,end_column=None,sample_id=None):
        self._file = file
        self._raw_data = tablib.Dataset().load(file.read())
        self.header_index = header_index
        self.data_index = data_index
        self.start_column = start_column
        self.end_column = end_column
        if sample_id:
            self._SAMPLE_ID = sample_id
        headers = self._raw_data[self._header_index]
        self._data = tablib.Dataset(*self._raw_data[self._data_index:], headers=headers)
        #If filtering columns
        if start_column and end_column:
            self._data = self._data.subset(cols=headers[start_column:end_column+1]) 
        elif start_column:
            self._data = self._data.subset(cols=headers[start_column:])
        elif end_column:
            self._data = self._data.subset(cols=headers[:end_column+1])
        print len(self._data)    
    @cached_property
    def _header_index(self):
        return self.header_index
    @cached_property
    def _data_index(self):
        return self.data_index if self.data_index else self._header_index + 1 
    @property
    def data(self):
        return self._data.dict
    def sample_ids(self):
        print 'sample_ids'
        return self._data[self._SAMPLE_ID]

class SRASampleSheet(SampleSheet):
    @cached_property
    def _header_index(self):
        for index, row in enumerate(self._raw_data):
            if '*sample_name'.upper() in row[0].upper():
                return index

class CoreSampleSheet(SampleSheet):
    def __init__(self,file,submission_type):
        super(CoreSampleSheet, self).__init__(file,submission_type.header_index,submission_type.data_index,submission_type.start_column,submission_type.end_column,submission_type.sample_identifier)
    