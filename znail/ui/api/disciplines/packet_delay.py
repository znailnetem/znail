import flask_restplus
import marshmallow

from znail.netem.disciplines import PacketDelay
from znail.netem.tc import Tc
from znail.ui import api
from znail.ui.util import NoneAttributes, handle_json_request


class PacketDelaySchema(marshmallow.Schema):
    milliseconds = marshmallow.fields.Integer(required=True, validate=lambda n: n > 0)


@api.route('/api/disciplines/packet_delay')
class PacketDelayResource(flask_restplus.Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tc = Tc.adapter('eth1')

    def get(self):
        delay = self.tc.disciplines.get('delay', NoneAttributes)
        return {'milliseconds': delay.milliseconds}, 200

    def post(self):

        def _post(data):
            disciplines = self.tc.disciplines
            disciplines['delay'] = PacketDelay(data['milliseconds'])
            self.tc.apply(disciplines)

        return handle_json_request(PacketDelaySchema(), _post)


@api.route('/api/disciplines/packet_delay/clear')
class ClearPacketDelayResource(flask_restplus.Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tc = Tc.adapter('eth1')

    def post(self):

        def _post(data):
            disciplines = self.tc.disciplines
            if 'delay' in disciplines:
                del disciplines['delay']
            self.tc.apply(disciplines)

        return handle_json_request(None, _post)
