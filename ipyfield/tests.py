from django.test import TestCase
from django.db.models import Model
from ipyfield.models import IPyField

class IPyFieldTests(TestCase):

    def setUp(self):
        class Obj(Model):
            '''Some kind of model'''
            field = IPyField()

        self.obj = Obj()

    def test_something(self):
        self.obj.field = '127.0.0.1'
        self.obj.field.strNormal()

