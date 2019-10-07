from django.conf import settings
from django.utils.module_loading import import_string

class PaymentType(object):
    id = 'PAYMENT_TYPE_ID' # must override this in subclass
    name = 'Payment Type Name' # must override this in subclass
    serializer_class = None # Must override this in subclass.  Should reference Django Rest Framework serializer.
    def __unicode__(self):
        return self.name

class PaymentTypeManager:
    def __init__(self):
        payment_types = getattr(settings,'PAYMENT_TYPES')
        self.payment_types = {}    
        for p in payment_types:
            p = import_string(p)
            self.payment_types[p.id]=p
    def get_payment_type(self,id):
        if self.payment_types.has_key(id):
            return self.payment_types[id]
        return None
    def get_choices(self):
        choices = ()
        for id, payment_type in self.payment_types.items():
            choices += ((id,payment_type.name),)
        return choices
