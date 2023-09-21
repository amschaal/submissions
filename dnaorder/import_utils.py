import urllib.request, json
from django.conf import settings
from dnaorder.models import Submission, SubmissionType
from django.conf.urls.static import static
import re

# from urllib import request

def post_json_data(url, data, headers={'Content-Type':'application/json'}):
    """
    POST data string to `url`, return page and headers
    """
    # if data is not in bytes, convert to it to utf-8 bytes
    data = json.dumps(data)
    bindata = data if type(data) == bytes else data.encode('utf-8')
    # need Request to pass headers
    req = urllib.request.Request(url, bindata, headers)
    resp = urllib.request.urlopen(req)
    return resp.read(), resp.getheaders()

def get_data(URL):
    with urllib.request.urlopen(URL) as url:
        print(URL)
        data = url if isinstance(url, str) else url.read().decode('utf-8')
        print(data)
        data = json.loads(data)#url.read().decode()
        return data

def get_submission(URL):
    return get_data(URL)

def parse_submission_id(URL):
    return re.findall(r'.*\/submissions\/([a-zA-Z0-9]+)\/?',URL)[0] #being lazy, just going to let error propagate.

# Only dealing with locally hosted submissions for now for simplicity
def import_submission_url(url, request=None):
    submission_id = parse_submission_id(url)
    from dnaorder.api.serializers import SubmissionSerializer
    from dnaorder.models import Submission
    submission = Submission.objects.get(id=submission_id)
    data = SubmissionSerializer(submission).data
    data.pop('lab', None)
    data['payment'] = {} # don't include payment
    data.pop('participants', None)
    data.pop('received_by', None)
    return data

# When we want to support importing from other submission systems, this will be necessary
def import_submission_url_remote(url, request=None):
    url = get_submission_api_url(url)
    submission = get_submission(url)
    submission.pop('lab', None)
    submission.pop('participants', None)
    submission.pop('received_by', None)
    return submission

def get_submission_api_url(url, request=None):
    if url[:-1] != '/':
        url += '/'
    if '/api/submissions/' in url:
        return url
    else:
        return url.replace('/submissions/','/server/api/submissions/') 

# Only dealing with locally hosted submission types and submissions for now for simplicity
def get_submission_schema(url): #takes either submission or submission type URL
    if url[:-1] != '/':
        url += '/'
    if '/submissions/' in url:
        return import_submission_url(url).get('submission_schema')
    type_id = re.findall(r'.*\/submission_types?\/([0-9]+)\/?',url)[0]
    from dnaorder.api.serializers import SubmissionTypeSerializer
    from dnaorder.models import SubmissionType
    submission_type = SubmissionType.objects.get(id=type_id)
    data = SubmissionTypeSerializer(submission_type).data
    return data.get('submission_schema')

# When we want to support importing from other submission systems, this will be necessary
def get_submission_schema_remote(url): #takes either submission or submission type URL
    if url[:-1] != '/':
        url += '/'
    if '/api/submission_types' in url:
        pass
    elif '/submissions/' in url:
        url = get_submission_api_url(url)
    elif '/submission_type/' in url:
        url = re.sub(r'(.+)\/[^\/]+\/submission_type\/(.+)', r'\1/server/api/submission_types/\2', url) # should be :domain/:lab_id/submission_type/:id
    data = get_data(url)
    return data.get('submission_schema')

def export_submission(submission, import_url):
    submission_url = submission.get_absolute_url(full_url=True)
    resp = post_json_data(import_url, {'url': submission_url})
