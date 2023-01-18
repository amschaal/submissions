"""
The API for PPMS is terrible and does not provide standard return codes formats.
Don't bother trying to make this pretty...
"""
import urllib
from django.conf import settings
PPMS_URL = getattr(settings,'PPMS_URL','https://ppms.us/ucdavis/pumapi/')
PPMS_AUTH_TOKEN = getattr(settings,'PPMS_AUTH_TOKEN')
def group_exists(unitlogin):
    params = {"action":"getgroup","unitlogin":unitlogin,"apikey":PPMS_AUTH_TOKEN}
    data = urllib.request.urlopen(PPMS_URL,urllib.parse.urlencode(params)).read()
    if len(data.split('\n')) > 1:
        return True
    return False



# #Python 3 POST
# from urllib import request, parse

# def test(params):
#     params['apikey'] = PPMS_AUTH_TOKEN
#     data = parse.urlencode(params).encode()
#     req =  request.Request(PPMS_URL, data=data) # this will make the method "POST"
#     resp = request.urlopen(req)
#     return resp
# # test({"action":"getservices"})