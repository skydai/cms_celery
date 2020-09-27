from __future__ import absolute_import, unicode_literals

from celery import chain

from cms_celery.openstack_tasks import o_add, o_mul

res = chain(o_add.s(2, 2), o_mul.si(5, 4), o_add.si(6, 9))()

# res = o_add.delay(2,2)
print res.get()


