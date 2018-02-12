import flask_restful

from znail.netem.healthcheck import perform_health_checks
from znail.ui import api


@api.route('/api/healthcheck')
class HealthCheckResource(flask_restful.Resource):

    def get(self):
        return perform_health_checks(), 200
