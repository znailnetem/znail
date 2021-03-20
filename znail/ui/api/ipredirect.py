import ipaddress

import flask_restplus
import marshmallow

from znail.netem.ipredirect import IpRedirect, IpRedirectDescriptor
from znail.ui import api
from znail.ui.util import json_request_handler


def _validate_port(n):
    return n > 0 and n < 65535


class IpRedirectSchema(marshmallow.Schema):
    ip = marshmallow.fields.Str(required=True)
    port = marshmallow.fields.Integer(required=True, validate=_validate_port)
    destination_ip = marshmallow.fields.Str(required=True)
    destination_port = marshmallow.fields.Integer(required=True, validate=_validate_port)
    protocol = marshmallow.fields.Str(required=True)

    @marshmallow.pre_load
    def validate_ip_fields(self, data):
        try:
            ipaddress.ip_address(data["ip"])
            ipaddress.ip_address(data["destination_ip"])
        except Exception as e:
            raise marshmallow.ValidationError(str(e))
        return data

    @marshmallow.pre_load
    def validate_protocol(self, data):
        choices = ["tcp", "udp"]
        if not data["protocol"] in choices:
            raise marshmallow.ValidationError("Protocol must be one of: {choices}".format(choices=choices))
        return data

    @marshmallow.post_load
    def prepare_descriptor(self, item):
        return IpRedirectDescriptor(
            item["ip"], item["port"], item["destination_ip"], item["destination_port"], item["protocol"]
        )


_ip_redirects = IpRedirect()
ip_redirect_schema = IpRedirectSchema(many=True)
ip_redirect_model = [
    api.model(
        "IpRedirect",
        {
            "ip": flask_restplus.fields.String(),
            "port": flask_restplus.fields.Integer(min=0, max=65535),
            "destination_ip": flask_restplus.fields.String(),
            "destination_port": flask_restplus.fields.Integer(min=0, max=65535),
            "protocol": flask_restplus.fields.String(),
        },
    )
]


@api.route("/api/ipredirect")
class IpRedirectResource(flask_restplus.Resource):
    @api.response(200, "Success", ip_redirect_model)
    def get(self):
        return [
            {
                "ip": redirect.ip,
                "port": int(redirect.port),
                "destination_ip": redirect.destination_ip,
                "destination_port": int(redirect.destination_port),
                "protocol": redirect.protocol,
            }
            for redirect in _ip_redirects.redirects
        ], 200

    @json_request_handler(ip_redirect_schema, ip_redirect_model)
    def post(self, data):
        _ip_redirects.apply(set(data))


@api.route("/api/ipredirect/clear")
class ClearIpRedirectResource(flask_restplus.Resource):
    @json_request_handler()
    def post(self, data):
        _ip_redirects.clear()
