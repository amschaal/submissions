from plugins import Plugin
from .forms import form
from .serializers import UCDChartstringPaymentType

class UCDPaymentPlugin(Plugin):
    ID = 'ucd_payment'
    FORM = form
    PAYMENT = UCDChartstringPaymentType
