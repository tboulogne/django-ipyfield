.. -*- restructuredtext -*-

django-ipyfield
===============

``ipyfield`` provides a model field for 
`django <https://www.djangoproject.com>`_
that allows the storage of an ip address as a "pretend" ``PositiveBigInt``
(currently ``varchar(39)`` until I can figure out how to get an unsigned 64bit
integer column across all supported DBs)
on the db side by using `IPy <http://pypi.python.org/pypi/IPy/>`_ to handle
conversion to an ``IPy.IP`` instance (or ``None``) on the python side. 

Wut?
----

In its way, it gives us a way to store both **ipv4** and **ipv6** consistently
without having to throw them in long charfields. Also, it gives us an easy way
to validate data as it comes in, while giving us access to additional meta
information (basically everything that makes 
`IPy <http://pypi.python.org/pypi/IPy/>`_ so awesome).


Installation
------------

Add this to your django project by installing with ``pip``: ::
    
    pip install django-ipyfield

or with ``easy_install``: ::

    easy_install django-ipyfield



Usage
-----

In your models, do something like the following: ::
    
    from django.db import models
    from ipyfield.models import IPyField

    class MyModel(models.Model):

        # the regular params should work well enough here
        ipaddr = IPyField()
        # ... and so on


From here, any assignments to ``obj.ipaddr`` can be considered a constructor
argument to a new ``IPy.IP`` instance. Anything ``IP()`` can use to make a new
object can be used.

When making queries, I added one extra piece of syntactical sugar. For 
``__in`` (range) lookups, you can pass a **CIDR** notation address range, for 
example: ::
    
    MyModel.objects.filter(ipaddr__in='10.0.0.0/24')

Currently you need to use this form of notation supported for this kind of 
query. For now, if you need to use a ``prefix-netmask`` style notation, pass it 
to ``IPy.IP`` yourself and use the resulting instance as your filter parameter.


TODOs
-----

* figure out how to build an appropriately sized integer field across all DBs.

Changelog
---------

0.1.6
    Added support for ``gt``, ``gte``, ``lt``, and ``lte`` lookups.
0.1.5
    Added south support.

0.1.4
    IPy.IP instance raises exception when compared to a non-IP instance. This
    becomes an issue when you get into ModelForm validation (didn't come up when
    only using the ORM) with regards to empty/null values. Fixed by subclassing
    (wrapping) IPy.IP.
0.1.3
    Basic field functionality in place.


