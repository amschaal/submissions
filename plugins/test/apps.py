from django.apps import AppConfig
from .forms import form

class TestConfig(AppConfig):
    name = 'plugins.test'
    form = form