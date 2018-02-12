import ipaddress

import flask_restful
import marshmallow

from znail.netem.dnsoverride import DnsOverrideDescriptor, DnsOverrides
from znail.ui import api
from znail.ui.util import handle_json_request


class DnsOverrideSchema(marshmallow.Schema):
    hostname = marshmallow.fields.Str(validate=marshmallow.validate.Length(min=2), required=True)
    ip_address = marshmallow.fields.Str(required=False)

    @marshmallow.pre_load
    def validate_ip_address(self, data):
        try:
            if data['ip_address']:
                ipaddress.ip_address(data['ip_address'])
        except Exception as e:
            raise marshmallow.ValidationError(str(e))
        return data

    @marshmallow.post_load
    def prepare_descriptor(self, item):
        return DnsOverrideDescriptor(item['hostname'], item['ip_address'])


_dns_overrides = DnsOverrides()


@api.route('/api/dnsoverride')
class DnsOverrideResource(flask_restful.Resource):

    def get(self):
        return [
            {
                'hostname': override.hostname,
                'ip_address': override.ip_address
            } for override in _dns_overrides.overrides
        ], 200

    def post(self):

        def _post(data):
            _dns_overrides.apply(set(data))

        return handle_json_request(DnsOverrideSchema(many=True), _post)


@api.route('/api/dnsoverride/clear')
class ClearDnsOverrideResource(flask_restful.Resource):

    def post(self):

        def _post(data):
            _dns_overrides.clear()

        return handle_json_request(None, _post)
