from flask import Blueprint
from flask.ext.restplus import Api


blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint,
    title='CMS Celery API',
    version='1.0',
    description='CMS Celery API',
)

# api = Api(
#     version='1.0',
#     title="CMS Celery API",
#     description="CMS Celery API",
# )

from api.v1.openstack import *
from api.v1.k8s import *
from api.v1.tasks import tasks
api.add_namespace(ostack)
api.add_namespace(k8s)
api.add_namespace(tasks)

