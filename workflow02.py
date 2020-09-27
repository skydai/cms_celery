from __future__ import absolute_import, unicode_literals

from celery import chain
from celery.result import AsyncResult

from cms_celery.openstack_tasks import o_add, o_mul

res = chain(o_add.s(2, 2), o_mul.s(5), o_add.si(6, 9))()
print res.get()

aa = AsyncResult(res.task_id, parent=res.parent.task_id)

print aa


