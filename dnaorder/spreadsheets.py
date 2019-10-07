from __builtin__ import file
import tablib
from django.utils.functional import cached_property
import pandas
from collections import OrderedDict
from dnaorder.models import Validator
import json
import string

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
        return self._data[self._SAMPLE_ID]

class SampleSheet(object):
    _SAMPLE_ID = '*sample_name'
    def __init__(self,file,header_index=0,skip_rows=None,start_column=None,end_column=None,sample_id=None,to_lower=True,max_rows=None):
        self._file = file
        self._errors = []
        usecols = None
        if start_column and end_column:
            usecols = '{0}:{1}'.format(start_column,end_column)
        elif end_column:
            usecols = end_column
#         if sample_id:
#             self._SAMPLE_ID = sample_id
        self.df = pandas.read_excel(file,header=header_index,usecols=usecols,sheet_name=0,dtype={self._SAMPLE_ID :str}).dropna(how='all')
        file.seek(0)

        self._SAMPLE_ID = self._SAMPLE_ID.lstrip('*')

        rename = {}
        for c in self.headers:
            if c.startswith('*'):
                rename[c]=c.lstrip('*')
        self.required_columns = rename.values()
        self.df.rename(columns=rename, inplace=True)
        if self._SAMPLE_ID in self.required_columns:
            self.required_columns.remove(self._SAMPLE_ID)

        if not self.df.size or self._SAMPLE_ID not in list(self.df.columns):
            return
        self.df.drop(self.df[self.df[self._SAMPLE_ID]=='nan'].index,inplace=True) #apparently blank sample ids are converted to the string 'nan', and are not dropped with "dropna".  Drop them here.
        #self.df.drop()
        
        
        if skip_rows or max_rows:
#             self.df = self.df.drop(self.df.index[range(0,skip_rows)])#df.index[2]
            self.df = self.df.iloc[skip_rows:max_rows]#df.index[2]
        
        
        if to_lower:
            self.df[self._SAMPLE_ID] = self.df[self._SAMPLE_ID].str.lower() 
        self.sample_df = self.df.set_index(self._SAMPLE_ID)
    @property
    def headers(self):
        return list(self.df.columns)
    @property
    def num_samples(self):
        return len(self.df)
    @property
    def not_null(self):
        return self.df.where((pandas.notnull(self.df)), None)
    @property
    def data(self):
        return self.get_data()
    @staticmethod
    def pages(df, page_size):
        """Yield successive paged dataframes from df."""
        for i in xrange(0, len(df), page_size):
            yield df.iloc[i:i + page_size]
    def get_data(self,exclude_columns=None,transpose=False,to_dict=True,page_size=0,not_null=True): #if page_size > 0, paginate
        if not_null:
            df = self.not_null
        else:
            df = self.df
        pages = None
        if exclude_columns:
            df = self.remove_cols(df, exclude_columns)
        if page_size > 0:
            pages = self.pages(df, page_size)
            if transpose:
                pages = [p.transpose() for p in pages]
            return [self.to_dict(page) for page in pages] if to_dict else pages
        if transpose:
            df = df.transpose()
        return self.to_dict(df) if to_dict else df
    @property
    def transposed(self):
        return self.get_data(transpose=True)
    @staticmethod
    def remove_cols(df,cols=[]):
        keep = [c for c in list(df) if c not in cols]
        return df[keep]
    @staticmethod
    def to_dict(df):
        return df.to_dict(orient='records',into=OrderedDict)
    def sample_ids(self):
        return self.df[self._SAMPLE_ID]
#     @property
#     def required_columns(self):
#         return [c for c in list(self.df.columns) if c.startswith('*') and c != self._SAMPLE_ID]
    def missing_values(self):
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
                    ids.append(id)
            if len(ids) > 0:
                self._errors.append({'column':v.field_id,'ids':ids, 'message':v.message})
        
        return self._errors
    def error_lookup(self):
        errors = {}
        for e in self._errors:
            if not e['column'] in errors:
                errors[e['column']] = {}
            for id in e['ids']:
                if not id in errors[e['column']]:
                    errors[e['column']][id] = []
                errors[e['column']][id]+=[e['message']]
            
        return errors
    def to_json(self,stringify=True):
        data = {'headers':self.headers,'data':self.data,'errors':self.error_lookup()}
        return json.dumps(data) if stringify else data
    def join(self,df):
        return self.sample_df.join(df.sample_df,how='left',rsuffix='_sra')
    @staticmethod
    def get_column_index(column_name=None):
        if not column_name:
            return None
        index = string.ascii_uppercase.find(column_name)
        return index if index > -1 else None

class SRASampleSheet(SampleSheet):
    def __init__(self,file,sample_id=None,main_samplesheet=None):
        #find header row based on sample id column name
        self._SAMPLE_ID = sample_id or self._SAMPLE_ID
        self._main_samplesheet = main_samplesheet
        df = pandas.read_excel(file)
        file.seek(0)
        header_index = list(df.iloc[:,0]).index(self._SAMPLE_ID) + 1
        #reset file pointer and init
        super(SRASampleSheet, self).__init__(file,header_index=header_index,sample_id=self._SAMPLE_ID)
    def validate(self):
        SampleSheet.validate(self)
        if self._main_samplesheet:
            diff = list(set(self.sample_ids()) - set(self._main_samplesheet.sample_ids()))
            if len(diff)>0:
                self._errors.append({'column':self._SAMPLE_ID,'ids':diff, 'message':'Sample ID not found in primary sample sheet.'})
        return self._errors
class CoreSampleSheetTemplate(SampleSheet):
    def __init__(self,submission_type):
        self.submission_type = submission_type
        super(CoreSampleSheetTemplate, self).__init__(self.submission_type.form.file,submission_type.header_index - 1,submission_type.skip_rows,submission_type.start_column,submission_type.end_column,submission_type.sample_identifier)

class CoreSampleSheet(SampleSheet):
    def __init__(self,file,submission_type):
        self.submission_type = submission_type
        self.template_samplesheet = CoreSampleSheetTemplate(self.submission_type)
        super(CoreSampleSheet, self).__init__(file,submission_type.header_index - 1,submission_type.skip_rows,submission_type.start_column,submission_type.end_column,submission_type.sample_identifier)
#         file.seek(0)
#         self._raw_data = tablib.Dataset().load(file.read())
#         file.seek(0)#       
#     @property
#     def submission_data(self):
#         if self.submission_type.has_submission_fields and self.submission_type.submission_header_row is not None and self.submission_type.submission_value_row:
#             return dict(
#                         zip(
#                             self._raw_data[self.submission_type.submission_header_row][self.get_column_index(self.submission_type.submission_start_column):self.get_column_index(self.submission_type.submission_end_column)+1],
#                             self._raw_data[self.submission_type.submission_value_row][self.get_column_index(self.submission_type.submission_start_column):self.get_column_index(self.submission_type.submission_end_column)+1]
#                         )
#                     )
    @property
    def headers_modified(self):
        if self.headers != self.template_samplesheet.headers:
            return True
        if self.required_columns != self.template_samplesheet.required_columns:
            return True
        return False


#Could probably leverage previous classes to do this.  Submission data is just a special case of only having 1 row of data and ignoring the rest.
class SubmissionData(object):
    def __init__(self, file, submission_type):
        self._file = file if file else submission_type.form.file
        usecols = None
        if submission_type.submission_start_column and submission_type.submission_end_column:
            usecols = '{0}:{1}'.format(submission_type.submission_start_column,submission_type.submission_end_column)
        elif submission_type.submission_end_column:
            usecols = submission_type.submission_end_column
        self._file.seek(0)
        self.df = pandas.read_excel(self._file,header=submission_type.submission_header_row-1,usecols=usecols,sheet_name=0)
        self._file.seek(0)
        self.df = self.df.iloc[submission_type.submission_skip_rows:1]#df.index[2]

        rename = {}
        for c in self.headers:
            if c.startswith('*'):
                rename[c]=c.lstrip('*')
        self.required_columns = rename.values()
        self.df.rename(columns=rename, inplace=True)
        if file:
            self.template = SubmissionData(None,submission_type) #kinda funky, but trying to use this class to get info about the template headers
    @property
    def data(self):
        return self.to_dict(self.df.where((pandas.notnull(self.df)), None))
    @staticmethod
    def to_dict(df):
        return df.to_dict(orient='records',into=OrderedDict)[0]
    @property
    def headers(self):
        return list(self.df.columns)
    @property
    def headers_modified(self):
        if self.headers != self.template.headers:
            return True
        if self.required_columns != self.template.required_columns:
            return True
        return False
    def validate(self):
        errors = {}
        data = self.data
        for id in self.required_columns:
            val = data.get(id,None)
            if pandas.isnull(val):
                errors[id] = 'This field is required.'
        validators = Validator.objects.filter(field_id__in=self.headers)
        for v in validators:
            val = data.get(v.field_id,None)
            if not pandas.isnull(val) and not v.is_valid(val):
                errors[v.field_id] = v.message
        return errors
    def to_json(self,stringify=True):
        data = {'headers':self.headers,'data':self.data,'errors':self.validate()}
        return json.dumps(data) if stringify else data