from dnaorder.models import Lab, Institution
from django.contrib.sites.shortcuts import get_current_site

def get_site_lab(request):
    return Lab.objects.get(site__id=get_current_site(request).id)

def get_site_institution(request):
    return Institution.objects.get(site__id=get_current_site(request).id)