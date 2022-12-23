from plugins import Plugin
from .forms import form

class TestPlugin(Plugin):
    ID = 'test'
    FORM = form