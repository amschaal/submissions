from django.conf import settings
from django.utils.module_loading import import_string
from django.conf.urls import url
from django.urls.conf import include
plugin_urls = []

class Plugin(object):
    def __init__(self, plugin_id):
        self.plugin_id = plugin_id
        try:
            self.url_patterns = import_string(self.plugin_id+'.urls.urlpatterns')
        except: #ModuleNotFoundError
            self.url_patterns = [] #Should we do something?
        try:
            self.form = import_string(self.plugin_id+'.forms.form')
        except: #ModuleNotFoundError
            self.form = None
        
class PluginManager():
    __instance = None
    def __new__(cls, val=None):
        if PluginManager.__instance is None:
            PluginManager.__instance = object.__new__(cls)
            PluginManager.__instance.url_patterns = []
            PluginManager.__instance.plugins = {}
            PluginManager.__instance.val = val
    #         PluginManager.__instance.configure_urls()
            for plugin in settings.PLUGINS:
                _plugin = Plugin(plugin)
                PluginManager.__instance.plugins[plugin] = _plugin
                PluginManager.__instance.url_patterns.append(url(r'^api/{}/'.format(plugin), include(_plugin.url_patterns)))
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
