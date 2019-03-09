import flask_restplus
import marshmallow

from znail.netem.disciplines import RateControl
from znail.netem.tc import Tc
from znail.ui import api
from znail.ui.util import NoneAttributes, handle_json_request


class PacketCorruptionSchema(marshmallow.Schema):
    kbit = marshmallow.fields.Integer(required=True, validate=lambda n: n > 0)
    latency_milliseconds = marshmallow.fields.Integer(required=True, validate=lambda n: n > 0)
    burst_bytes = marshmallow.fields.Integer(required=True, validate=lambda n: n > 0)


@api.route('/api/disciplines/packet_rate_control')
class PacketRateControlResource(flask_restplus.Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tc = Tc.adapter('eth1')

    def get(self):
        rate_control = self.tc.disciplines.get('rate', NoneAttributes)
        return {
            'kbit': rate_control.kbit,
            'latency_milliseconds': rate_control.latency_milliseconds,
            'burst_bytes': rate_control.burst_bytes,
        }, 200

    def post(self):

        def _post(data):
            disciplines = self.tc.disciplines
            disciplines['rate'] = RateControl(
                data['kbit'], data['latency_milliseconds'], data['burst_bytes'])
            self.tc.apply(disciplines)

        return handle_json_request(PacketCorruptionSchema(), _post)


@api.route('/api/disciplines/packet_rate_control/clear')
class ClearPacketRateControlResource(flask_restplus.Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tc = Tc.adapter('eth1')

    def post(self):

        def _post(data):
            disciplines = self.tc.disciplines
            if 'rate' in disciplines:
                del disciplines['rate']
            self.tc.apply(disciplines)

        return handle_json_request(None, _post)
