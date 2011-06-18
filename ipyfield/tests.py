from django.test import TestCase
from django.db.models import Model
from ipyfield.models import IPyField
from IPy import IP


class DummyModel(Model):
    field = IPyField()

class IPyFieldTests(TestCase):

    def setUp(self):
        self.obj = DummyModel()

    def test_iptype(self):
        self.obj.field = '127.0.0.1'
        self.assertEqual(self.obj.field.iptype(),'PRIVATE')
        self.obj.field = '100.80.90.100'
        self.assertEqual(self.obj.field.iptype(), 'PUBLIC')


    def test_lookups_in_CIDR(self):
        ip_block = IP('127.0.0.0/28')
        [DummyModel.objects.create(field=ip) for ip in ip_block]
        self.assertEqual(len(ip_block), DummyModel.objects.count())
        self.assertTrue(DummyModel.objects.count() > 
               DummyModel.objects.filter(field__in=IP('127.0.0.0/30'))\
               .count())


