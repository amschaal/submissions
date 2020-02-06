import urllib.request, json
from django.conf import settings
from dnaorder.models import Submission, SubmissionType
from django.conf.urls.static import static

def get_submission(URL):
    with urllib.request.urlopen(URL) as url:
        print(URL)
        data = url if isinstance(url, str) else url.read().decode('utf-8')
        print(data)
        data = json.loads(data)#url.read().decode()
        return data

def import_submission_url(url):
    url = get_submission_api_url(url)
    submission = get_submission(url)
    submission.pop('lab', None)
    submission.pop('participants', None)
    print(submission)
    return submission

def get_submission_api_url(url):
    if url[:-1] != '/':
        url += '/'
    if '/api/submissions/' in url:
        return url
    else:
        return url.replace('/submissions/','/server/api/submissions/')
