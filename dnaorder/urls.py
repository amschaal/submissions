"""dnaorder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from api.urls import urlpatterns as api_urlpatterns

import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.submit, name='submit'),
    url(r'^submissions/$', views.submissions, name='submissions'),
    url(r'^submission_types/$', views.submission_types, name='submission_types'),
    url(r'^submission_types/create/$', views.create_update_submission_type, name='create_submission_type'),
    url(r'^submission_types/(?P<id>\d+)/update/$', views.create_update_submission_type, name='update_submission_type'),
    url(r'^submission_types/(?P<id>\d+)/versions/$', views.submission_type_versions, name='submission_type_versions'),
    url(r'^validators/$', views.validators, name='validators'),
    url(r'^validators/create/$', views.create_update_validator, name='create_validator'),
    url(r'^validators/(?P<id>\d+)/update/$', views.create_update_validator, name='update_validator'),
    url(r'^submissions/(?P<id>[0-9a-f-]+)/$', views.submission, name='submission'),
    url(r'^submissions/(?P<id>[0-9a-f-]+)/print/$', views.print_submission, name='print_submission'),
    url(r'^submissions/(?P<id>[0-9a-f-]+)/print/custom/$', views.customize_print, name='customize_print'),
    url(r'^submissions/(?P<id>[0-9a-f-]+)/confirm/$', views.confirm_submission, name='confirm_submission'),
    url(r'^submissions/(?P<id>[0-9a-f-]+)/update/$', views.update_submission, name='update_submission'),
    url(r'^submissions/(?P<id>[0-9a-f-]+)/download/$', views.download, name='download'),
    url(r'^api/', include(api_urlpatterns)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
