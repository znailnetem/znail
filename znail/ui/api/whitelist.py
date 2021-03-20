import ipaddress

import flask_restplus
import marshmallow

from znail.netem.tc import Tc
from znail.ui import api
from znail.ui.util import json_request_handler


class WhiteListSchema(marshmallow.Schema):
    ip_address = marshmallow.fields.Str(required=True)

    @marshmallow.pre_load
    def validate_ip_address(self, data):
        try:
            ipaddress.ip_address(data["ip_address"])
        except Exception as e:
            raise marshmallow.ValidationError(str(e))
        return data


white_list_schema = WhiteListSchema(many=True)
white_list_model = [
    api.model(
        "WhiteList",
        {
            "ip_address": flask_restplus.fields.String(),
        },
    )
]


@api.route("/api/whitelist")
class WhiteListResource(flask_restplus.Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._tc = Tc.adapter("eth1")

    @api.response(200, "Success", white_list_model)
    def get(self):
        return [{"ip_address": ip_address} for ip_address in self._tc.whitelist], 200

    @json_request_handler(white_list_schema, white_list_model)
    def post(self, data):
        self._tc.whitelist = list(set([entry["ip_address"] for entry in data]))
        self._tc.apply(self._tc.disciplines)


@api.route("/api/whitelist/clear")
class ClearWhiteListResource(flask_restplus.Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._tc = Tc.adapter("eth1")

    @json_request_handler()
    def post(self, data):
        self._tc.whitelist = []
        self._tc.apply(self._tc.disciplines)
