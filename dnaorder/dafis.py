from urllib.request import urlopen
import json
def validate_dafis(acct_string):
    try:
        chart,account = acct_string.split('-',1)
    except:
        return False
#         raise forms.ValidationError("The account is invalid.  Please ensure that the chart and account are valid and in the form 'chart-account'.")
    URL = "https://kfs.ucdavis.edu/kfs-prd/remoting/rest/fau/account/%s/%s/isvalid" % (chart,account)
    valid = None
    json.loads(urlopen(URL).read().decode())
    try:
        valid = json.loads(urlopen(URL).read().decode())
    except Exception as e:
        return False
    return valid
