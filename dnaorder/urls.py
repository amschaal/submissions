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
# from django.conf.urls import url, include
from django.urls import include, re_path
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
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^api/submissions/(?P<id>[0-9a-f-]+)/download/$', views.download, name='download'),
    re_path(r'^api/', include(api_urlpatterns)),
    re_path(r'^api2/', include(api_urlpatterns)), #delete this, just testing CI/CD
    re_path(r'^api/billing/', include(billing_urlpatterns)),
    re_path(r'^api/validate/$', views.validate_data, name='validate'),
    re_path(r'^api/login/$', views.login_view, name='api_login'),
    re_path(r'^api/logout/$', views.logout_view, name='logout'),
    re_path(r'^api/get_user/$', views.get_user, name='get_user'),
    re_path(r'^accounts/login/$', views.login, name='login'),
    # url(r'^accounts/logout/$', views.logout, name='logout'),
    re_path(r'^accounts/logout/$', auth_views.LogoutView.as_view(), name='logout'),
    re_path(r'^social/', include('social_django.urls', namespace='social')),
    re_path(r'^test/$', views.test)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


urlpatterns += PluginManager().urls
