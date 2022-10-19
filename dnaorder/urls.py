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
from dnaorder.api.urls import urlpatterns as api_urlpatterns
from billing.api.urls import urlpatterns as billing_urlpatterns
from django.contrib.auth import views as auth_views

from dnaorder import views
from django.utils.module_loading import import_string
from plugins import PluginManager

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/submissions/(?P<id>[0-9a-f-]+)/download/$', views.download, name='download'),
    url(r'^api/', include(api_urlpatterns)),
    url(r'^api2/', include(api_urlpatterns)), #delete this, just testing CI/CD
    url(r'^api/billing/', include(billing_urlpatterns)),
    url(r'^api/validate/$', views.validate_data, name='validate'),
    url(r'^api/login/$', views.login_view, name='api_login'),
    url(r'^api/logout/$', views.logout_view, name='logout'),
    url(r'^api/get_user/$', views.get_user, name='get_user'),
    url(r'^accounts/login/$', views.login, name='login'),
    url(r'^accounts/logout/$', views.logout, name='logout'),
    url(r'^test/$', views.test)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


urlpatterns += PluginManager().urls
