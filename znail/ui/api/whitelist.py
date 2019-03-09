import ipaddress

import flask_restplus
import marshmallow

from znail.netem.tc import Tc
from znail.ui import api
from znail.ui.util import handle_json_request


class WhiteListSchema(marshmallow.Schema):
    ip_address = marshmallow.fields.Str(required=True)

    @marshmallow.pre_load
    def validate_ip_address(self, data):
        try:
            ipaddress.ip_address(data['ip_address'])
        except Exception as e:
            raise marshmallow.ValidationError(str(e))
        return data


@api.route('/api/whitelist')
class WhiteListResource(flask_restplus.Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._tc = Tc.adapter('eth1')

    def get(self):
        return self._tc.whitelist, 200

    def post(self):

        def _post(data):
            self._tc.whitelist = list(set([entry['ip_address'] for entry in data]))
            self._tc.apply(self._tc.disciplines)

        return handle_json_request(WhiteListSchema(many=True), _post)


@api.route('/api/whitelist/clear')
class ClearWhiteListResource(flask_restplus.Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._tc = Tc.adapter('eth1')

    def post(self):

        def _post(data):
            self._tc.whitelist = []
            self._tc.apply(self._tc.disciplines)

        return handle_json_request(None, _post)
