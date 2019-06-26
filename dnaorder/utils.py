from dnaorder.models import Lab
from django.contrib.sites.shortcuts import get_current_site

def get_site_lab(request):
    return Lab.objects.get(site__id=get_current_site(request).id)