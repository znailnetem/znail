import ipaddress

import flask_restplus
import marshmallow

from znail.netem.dnsoverride import DnsOverrideDescriptor, DnsOverrides
from znail.ui import api
from znail.ui.util import json_request_handler


class DnsOverrideSchema(marshmallow.Schema):
    hostname = marshmallow.fields.Str(validate=marshmallow.validate.Length(min=2), required=True)
    ip_address = marshmallow.fields.Str(required=False)

    @marshmallow.pre_load
    def validate_ip_address(self, data):
        try:
            if data["ip_address"]:
                ipaddress.ip_address(data["ip_address"])
        except Exception as e:
            raise marshmallow.ValidationError(str(e))
        return data

    @marshmallow.post_load
    def prepare_descriptor(self, item):
        return DnsOverrideDescriptor(item["hostname"], item["ip_address"])


_dns_overrides = DnsOverrides()
dns_override_schema = DnsOverrideSchema(many=True)
dns_override_model = [
    api.model(
        "DnsOverride",
        {
            "hostname": flask_restplus.fields.String(),
            "ip_address": flask_restplus.fields.String(),
        },
    )
]


@api.route("/api/dnsoverride")
class DnsOverrideResource(flask_restplus.Resource):
    @api.response(200, "Success", dns_override_model)
    def get(self):
        return [
            {"hostname": override.hostname, "ip_address": override.ip_address} for override in _dns_overrides.overrides
        ], 200

    @json_request_handler(dns_override_schema, dns_override_model)
    def post(self, data):
        _dns_overrides.apply(set(data))


@api.route("/api/dnsoverride/clear")
class ClearDnsOverrideResource(flask_restplus.Resource):
    @json_request_handler()
    def post(self, data):
        _dns_overrides.clear()
