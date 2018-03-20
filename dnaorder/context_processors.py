from django.conf import settings

def url_processor(request):
    return {'BASE_URI': settings.BASE_URI}