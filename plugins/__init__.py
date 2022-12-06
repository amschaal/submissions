from django.conf import settings
from django.utils.module_loading import import_string
from django.conf.urls import url
from django.urls.conf import include
from functools import wraps
plugin_urls = []

class Plugin(object):
    def __init__(self, plugin_id):
        self.plugin_id = plugin_id
        try:
            self.url_patterns = import_string('plugins.{}.urls.urlpatterns'.format(self.plugin_id))
        except Exception as e: #ModuleNotFoundError
            if plugin_id == 'ppms':
                raise e
            self.url_patterns = [] #Should we do something?
        try:
            self.form = import_string('plugins.{}.forms.form'.format(self.plugin_id))
        except: #ModuleNotFoundError
            self.form = None
        
class PluginManager():
    __instance = None
    def __new__(cls, val=None):
        if PluginManager.__instance is None or True:
            PluginManager.__instance = object.__new__(cls)
            PluginManager.__instance.url_patterns = []#[url(r'^api/plugins/{}/submissions/(?P<submission_id>[0-9a-f-]+)/'.format('ppms'), include('plugins.{}.urls'.format('ppms')))]
            PluginManager.__instance.plugins = {}
            PluginManager.__instance.val = val
    #         PluginManager.__instance.configure_urls()
            for plugin in settings.PLUGINS:
                _plugin = Plugin(plugin)
                PluginManager.__instance.plugins[plugin] = _plugin
                PluginManager.__instance.url_patterns.append(url(r'^api/plugins/{}/submissions/(?P<submission_id>[0-9a-f-]+)/'.format(plugin), include(_plugin.url_patterns)))
                # try:
                #     PluginManager.__instance.url_patterns.append(url(r'^plugins/{}/'.format(plugin), include('plugins.{}.urls'.format(plugin))))
                # except:
                #     pass
        return PluginManager.__instance
#     def configure_urls(self):
#         self.__instance.url_patterns = []
#         for plugin in settings.PLUGINS:
#             try:
#                 print(plugin, plugin+'.urls.urlpatterns')
#                 plugin_patterns = import_string(plugin+'.urls.urlpatterns')
#                 self.__instance.url_patterns.append(url(r'^api/{}/'.format(plugin), include(plugin_patterns)))
#             except: #ModuleNotFoundError
#                 pass #Should we do something?
    @property
    def urls(self):
        return self.__instance.url_patterns
    def get_plugin(self, plugin_id):
        return self.__instance.plugins.get(plugin_id)


# This decorator will take the submission_id from the url, get the submission, and pass it into the original view.  Optionally require ALL or ANY permissions.
def plugin_submission_decorator(permissions=[], all=True):
    from dnaorder.models import Submission
    from rest_framework.exceptions import PermissionDenied
    def wrapper(view_func):
        @wraps(view_func)
        def wrapped(request, *args, **kwargs):
            submission = Submission.objects.get(id=kwargs.pop('submission_id'))
            if not submission.has_permission(request.user, permissions, all):
                raise PermissionDenied('The current user does not have permission to perform this action.')
            kwargs['submission']  = submission
            return view_func(request, *args, **kwargs)
        return wrapped
    return wrapper