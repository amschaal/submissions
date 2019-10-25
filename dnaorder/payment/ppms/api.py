"""
The API for PPMS is terrible and does not provide standard return codes formats.
Don't bother trying to make this pretty...
"""
import urllib
from django.conf import settings
PPMS_URL = getattr(settings,'PPMS_URL','https://ppms.us/ucdavis/pumapi/')
PPMS_AUTH_TOKEN = getattr(settings,'PPMS_AUTH_TOKEN')
# action=getgroup&unitlogin=lfroenicke@ucdavis.edu&apikey=9Uwx6KJYdxNLSgMz" "https://ppms.us/ucdavis-test/pumapi/
# urllib2.urlopen('https://ppms.us/ucdavis-test/pumapi/',urllib.urlencode({'action':'getgroup','unitlogin':'lfroenicke@ucdavis.edu','apikey':'9Uwx6KJYdxNLSgMz'})).read()
def group_exists(unitlogin):
    params = {"action":"getgroup","unitlogin":unitlogin,"apikey":PPMS_AUTH_TOKEN}
    data = urllib.request.urlopen(PPMS_URL,urllib.parse.urlencode(params)).read()
    if len(data.split('\n')) > 1:
        return True
    return False
