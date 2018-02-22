from __builtin__ import file
import tablib
from django.utils.functional import cached_property
import pandas
from psycopg2.tests.testutils import skip_after_libpq
from collections import OrderedDict
from dnaorder.models import Validator

class SampleSheetTablib(object):
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

class SampleSheet(object):
    _SAMPLE_ID = '*sample_name'
    def __init__(self,file,header_index=0,skip_rows=None,end_column=None,sample_id=None):
        self._file = file
        self.df = pandas.read_excel(file,header=header_index,usecols=end_column)
        file.seek(0)
        
        if skip_rows:
            self.df = self.df.drop(self.df.index[range(0,skip_rows)])#df.index[2]
        if sample_id:
            self._SAMPLE_ID = sample_id
        self._SAMPLE_ID = self._SAMPLE_ID.lstrip('*')

        rename = {}
        for c in self.headers:
            if c.startswith('*'):
                rename[c]=c.lstrip('*')
        self.required_columns = rename.values()
        self.df.rename(columns=rename, inplace=True)
        if self._SAMPLE_ID in self.required_columns:
            self.required_columns.remove(self._SAMPLE_ID)
        
        self.sample_df = self.df.set_index(self._SAMPLE_ID)
        self._errors = []
    @property
    def headers(self):
        return list(self.df.columns)
    @property
    def data(self):
        df1 = self.df.where((pandas.notnull(self.df)), None)
        return df1.to_dict(orient='records',into=OrderedDict)
    def sample_ids(self):
        return self.df[self._SAMPLE_ID]
#     @property
#     def required_columns(self):
#         return [c for c in list(self.df.columns) if c.startswith('*') and c != self._SAMPLE_ID]
    def missing_values(self):
        print 'missing values'
        missing = OrderedDict()
        for r in self.required_columns:
            ids = self.sample_df[self.sample_df[r].isnull()].index.values
            if len(ids) > 0:
                missing[r] = ids
        return missing
    def validate(self):
        duplicated = list(set(self.df[self._SAMPLE_ID][self.df.duplicated(self._SAMPLE_ID)]))
        if len(duplicated) > 0:
            self._errors.append({'column':self._SAMPLE_ID,'ids':duplicated, 'message':'There are duplicated sample ids.'})
        
        missing = self.missing_values()
        for col, ids in missing.items():
            self._errors.append({'column':col,'ids':ids, 'message':'This field is required.'})
        
        validators = Validator.objects.filter(field_id__in=self.headers)
        for v in validators:
            ids = []
            for id, r in self.sample_df[v.field_id].items():
                if not pandas.isnull(r) and not v.is_valid(r):
                    print r
                    ids.append(id)
            if len(ids) > 0:
                self._errors.append({'column':v.field_id,'ids':ids, 'message':v.message})
        
        return self._errors
class SRASampleSheet(SampleSheet):
    def __init__(self,file,sample_id=None):
        #find header row based on sample id column name
        self._SAMPLE_ID = sample_id or self._SAMPLE_ID
        df = pandas.read_excel(file)
        file.seek(0)
        header_index = list(df.iloc[:,0]).index(self._SAMPLE_ID) + 1
        #reset file pointer and init
        super(SRASampleSheet, self).__init__(file,header_index=header_index,sample_id=self._SAMPLE_ID)

class CoreSampleSheet(SampleSheet):
    def __init__(self,file,submission_type):
        self.submission_type = submission_type
        super(CoreSampleSheet, self).__init__(file,submission_type.header_index,submission_type.skip_rows,submission_type.end_column,submission_type.sample_identifier)
    @property
    def template_headers(self):
        template_df = CoreSampleSheet(self.submission_type.form.file,self.submission_type)
        print 'template headers'
        return template_df.headers
        