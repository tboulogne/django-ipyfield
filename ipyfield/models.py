from django.db import models
from IPy import IP

class IPyField(models.Field):
    """
    Handles conversion between int db column and IPy.IP instance.
    """
    
    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        if not value: 
            return None
        elif isinstance(value, IP):
            return value
        else:
            return IP(value)

    def get_prep_value(self, value):
        value = self.to_python(value)
        if not value:
            return None
        return value.int()

    def get_prep_lookup(self, lookup_type, value):
        if lookup_type == 'in':
            if isinstance(value, str) and '/' in value:
                # convert to CIDR iter
                value = IP(value)
            return [self.get_prep_value(v) for v in value]
        else: 
            return self.get_prep_value(value)

    def get_internal_type(self):
        return 'BigIntegerField'

