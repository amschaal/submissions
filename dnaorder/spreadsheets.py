from __builtin__ import file
import tablib

class SampleSheet(object):
    def __init__(self,file):
        self._file = file
        self._raw_data = tablib.Dataset().load(file.read())
        header_index = self._header_index
        self._data = tablib.Dataset(*self._raw_data[header_index+1:], headers=self._raw_data[header_index])
    @property
    def _header_index(self):
        raise NotImplementedError('Must return index of header row')
    @property
    def data(self):
        return self._data.dict

class SRASampleSheet(SampleSheet):
    @property
    def _header_index(self):
        for index, row in enumerate(self._raw_data):
            if '*sample_name'.upper() in row[0].upper():
                return index
    