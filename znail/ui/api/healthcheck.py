import flask_restplus

from znail.netem.healthcheck import perform_health_checks
from znail.ui import api


@api.route('/api/healthcheck')
class HealthCheckResource(flask_restplus.Resource):

    def get(self):
        return perform_health_checks(), 200
