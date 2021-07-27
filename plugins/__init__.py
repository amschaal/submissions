from django.conf import settings
from django.utils.module_loading import import_string
from django.conf.urls import url
from django.urls.conf import include
plugin_urls = []

# class Plugin(object):
#     def __init__(self, plugin_id):
#         self.plugin_id = plugin_id
#         try:
#             self.url_patterns = import_string(self.plugin_id+'.urls.urlpatterns')
#         except: #ModuleNotFoundError
#             pass #Should we do something?
        
class PluginManager():
    __instance = None
    def __new__(cls, val=None):
        if PluginManager.__instance is None:
            PluginManager.__instance = object.__new__(cls)
        PluginManager.__instance.val = val
        PluginManager.__instance.configure_urls()
        return PluginManager.__instance
    def configure_urls(self):
        self.__instance.url_patterns = []
        for plugin in settings.PLUGINS:
            try:
                print(plugin, plugin+'.urls.urlpatterns')
                plugin_patterns = import_string(plugin+'.urls.urlpatterns')
                self.__instance.url_patterns.append(url(r'^api/{}/'.format(plugin), include(plugin_patterns)))
            except: #ModuleNotFoundError
                pass #Should we do something?
    @property
    def urls(self):
        return self.__instance.url_patterns
