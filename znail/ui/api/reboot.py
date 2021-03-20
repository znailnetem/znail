import weakref

import flask_restplus
from flask.ctx import after_this_request

from znail.netem.util import reboot
from znail.ui import api

reboot_model = [api.model("Reboot", {})]


@api.route("/api/reboot")
class RebootResource(flask_restplus.Resource):
    @api.response(200, "Success", reboot_model)
    def get(self):
        @after_this_request
        def do_reboot(response):
            weakref.finalize(response, reboot)
            response.headers["Location"] = "/"
            return response

        return {"message": "ok"}, 301
