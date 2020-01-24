import urllib.request, json
from django.conf import settings
from dnaorder.models import Submission, SubmissionType
from django.conf.urls.static import static

def get_submission(URL):
    with urllib.request.urlopen(URL) as url:
        data = url if isinstance(url, str) else url.read().decode('utf-8')
        data = json.loads(data)#url.read().decode()
        return data

def import_submission_url(url):
    submission = get_submission(url)
    print(submission)
    return submission
