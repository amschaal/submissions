def url_processor(request):
    return {'BASE_URI': request.build_absolute_uri('/').rstrip('/')}