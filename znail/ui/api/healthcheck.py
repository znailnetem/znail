import flask_restplus

from znail.netem.healthcheck import perform_health_checks
from znail.ui import api

health_check_model = [
    api.model(
        "HealthCheck",
        {
            "name": flask_restplus.fields.String(),
            "result": flask_restplus.fields.Integer(),
        },
    )
]


@api.route("/api/healthcheck")
class HealthCheckResource(flask_restplus.Resource):
    @api.response(200, "Success", health_check_model)
    def get(self):
        return perform_health_checks(), 200
