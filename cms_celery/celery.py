from __future__ import absolute_import, unicode_literals
from celery import Celery
#
# BROKER_URL = 'redis://127.0.0.1:6379'
# CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
# CELERY_TIMEZONE = 'Asia/Shanghai'


app = Celery('cms_celery')
app.config_from_object('celeryconfig')

# app = Celery('cms_celery', broker=BROKER_URL, backend=CELERY_RESULT_BACKEND, include=['cms_celery.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=7200,
)

if __name__ == '__main__':
    app.start()