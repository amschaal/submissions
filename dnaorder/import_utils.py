import urllib.request, json
from django.conf import settings
from dnaorder.models import Submission, SubmissionType
from django.conf.urls.static import static

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

def import_submission_url(url):
    url = get_submission_api_url(url)
    submission = get_submission(url)
    submission.pop('lab', None)
    submission.pop('participants', None)
    submission.pop('received_by', None)
    print(submission)
    return submission

def get_submission_api_url(url):
    if url[:-1] != '/':
        url += '/'
    if '/api/submissions/' in url:
        return url
    else:
        return url.replace('/submissions/','/server/api/submissions/')

def get_submission_schema(url): #takes either submission or submission type URL
    if url[:-1] != '/':
        url += '/'
    if '/submissions/' in url:
        url = get_submission_api_url(url)
    elif '/submission_type/' in url:
        url = url.replace('/submission_type/','/server/api/submission_types/')
    data = get_data(url)
    return data.get('submission_schema')

def export_submission(submission, import_url):
    submission_url = submission.get_absolute_url(full_url=True)
    resp = post_json_data(import_url, {'url': submission_url})
