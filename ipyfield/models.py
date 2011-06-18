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
        value = self.to_python(value) # Ensure we have IP instance or None
        if lookup_type == 'exact':
            return self.get_prep_value(value)
        elif lookup_type == 'in':
            return [self.get_prep_value(v) for v in value]
        else:
            raise TypeError('Lookup type %r not supported.' % lookup_type)

    def get_internal_type(self):
        return 'BigIntegerField'

