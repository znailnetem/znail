import flask_restful
import marshmallow

from znail.netem.disciplines import PacketLoss
from znail.netem.tc import Tc
from znail.ui import api
from znail.ui.util import NoneAttributes, handle_json_request


class PacketLossSchema(marshmallow.Schema):
    percent = marshmallow.fields.Float(required=True, validate=lambda n: n >= 0 and n <= 100)


@api.route('/api/disciplines/packet_loss')
class PacketLossResource(flask_restful.Resource):

    def __init__(self):
        self.tc = Tc.adapter('eth1')

    def get(self):
        loss = self.tc.disciplines.get('loss', NoneAttributes)
        return {'percent': loss.percent}, 200

    def post(self):

        def _post(data):
            disciplines = self.tc.disciplines
            disciplines['loss'] = PacketLoss(data['percent'])
            self.tc.apply(disciplines)

        return handle_json_request(PacketLossSchema(), _post)


@api.route('/api/disciplines/packet_loss/clear')
class ClearPacketLossResource(flask_restful.Resource):

    def __init__(self):
        self.tc = Tc.adapter('eth1')

    def post(self):

        def _post(data):
            disciplines = self.tc.disciplines
            if 'loss' in disciplines:
                del disciplines['loss']
            self.tc.apply(disciplines)

        return handle_json_request(None, _post)
