from django.conf import settings
from django.utils.module_loading import import_string
from django.conf.urls import url
from django.urls.conf import include
from functools import wraps
from rest_framework import serializers
import sys, copy
plugin_urls = []

FORM_ACCESS_INSTITUTION = 'INSTITUTION_FORM'
FORM_ACCESS_LAB = 'INSTITUTION_FORM'
# FORM_TYPE_ANY = 'ANY'

class Plugin(object):
    ID = None
    SUBMISSION_URLS = None
    FORM = None
    PAYMENT = None
    def __init__(self):
        self.form = self.FORM
    @property
    def institution_form(self):
        form = copy.deepcopy(self.form)
        for namespace in ['public', 'private']: 
            for field, definition in self.form[namespace]['properties'].items():
                if 'restrict_to' in definition and FORM_ACCESS_INSTITUTION not in definition['restrict_to']:
                    del form[namespace]['properties'][field]
                    if field in form[namespace]['order']:
                        form[namespace]['order'].remove(field)
                    if field in form[namespace]['required']:
                        form[namespace]['required'].remove(field)
        return form

class SubmissionPlugin:
    def __init__(self, plugin_id, submission):
        self.plugin_id = plugin_id
        self.submission = submission
        self.data = self.submission.plugin_data.get(self.plugin_id,{})
    def save(self):
        self.submission.save() 
    @property
    def settings(self):
        return self.submission.lab.get_plugin_settings(private=True).get(self.plugin_id, {})

class PaymentType(object):
    id = 'PAYMENT_TYPE_ID' # must override this in subclass
    name = 'Payment Type Name' # must override this in subclass
    serializer_class = None # Must override this in subclass.  Should reference Django Rest Framework serializer.
    def __unicode__(self):
        return self.name

class BasePaymentSerializer(serializers.Serializer):
    def __init__(self, instance=None, data=..., **kwargs):
        self._plugin_id = kwargs.pop('plugin_id')
        self.fields['plugin_id'] = serializers.CharField(default=self._plugin_id)
        sys.stderr.write('Serializer: {}\n'.format(self._plugin_id))
        super().__init__(instance, data, **kwargs)

class PluginManager():
    __instance = None
    def __new__(cls, PLUGINS=None, val=None):
        # sys.stderr.write('Calling PluginManager.__new__\n')
        if PluginManager.__instance is None:
            # sys.stderr.write('Instantiating.__instance!!!!\n')
            if not PLUGINS:
                PLUGINS = settings.PLUGINS
            PluginManager.__instance = object.__new__(cls)
            PluginManager.__instance.url_patterns = []#[url(r'^api/plugins/{}/submissions/(?P<submission_id>[0-9a-f-]+)/'.format('ppms'), include('plugins.{}.urls'.format('ppms')))]
            PluginManager.__instance.plugins = {}
            PluginManager.__instance.payment_types = {}
            PluginManager.__instance.val = val
    #         PluginManager.__instance.configure_urls()
            for plugin in PLUGINS:
                try:
                    _plugin = import_string(plugin)()
                    PluginManager.__instance.plugins[_plugin.ID] = _plugin
                    if _plugin.SUBMISSION_URLS:
                        PluginManager.__instance.url_patterns.append(url(r'^api/plugins/(?P<plugin_id>{})/submissions/(?P<submission_id>[0-9a-f-]+)/'.format(_plugin.ID), include(_plugin.SUBMISSION_URLS)))
                    if _plugin.PAYMENT:
                    #    PluginManager.__instance.payment_types[_plugin.PAYMENT.id]=_plugin.PAYMENT
                        PluginManager.__instance.payment_types[_plugin.ID]=_plugin.PAYMENT
                except:
                    sys.stderr.write('Unable to initialize plugin {}!\n'.format(plugin))
        # else:
        #     sys.stderr.write('***CACHED PluginManager.__intance***\n')
        return PluginManager.__instance
    @property
    def urls(self):
        return self.__instance.url_patterns
    def get_plugin(self, plugin_id):
        return self.__instance.plugins.get(plugin_id)
    def get_payment_type(self,id):
        if  id in self.payment_types:
            return self.payment_types[id]
        return None
    def payment_type_choices(self):
        choices = ()
        for id, payment_type in self.payment_types.items():
            choices += ((id,payment_type.name),)
        return choices
    @property
    def plugins_ids(self):
        return self.plugins.keys()


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
            plugin = SubmissionPlugin(kwargs.pop('plugin_id'), submission)
            kwargs['submission']  = submission
            kwargs['plugin'] = plugin
            return view_func(request, *args, **kwargs)
        return wrapped
    return wrapper