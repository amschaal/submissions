from dnaorder.utils import get_base_uri

def url_processor(request):
    return {'BASE_URI': get_base_uri(request)}