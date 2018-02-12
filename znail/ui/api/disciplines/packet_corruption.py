import flask_restful
import marshmallow

from znail.netem.disciplines import PacketCorruption
from znail.netem.tc import Tc
from znail.ui import api
from znail.ui.util import NoneAttributes, handle_json_request


class PacketCorruptionSchema(marshmallow.Schema):
    percent = marshmallow.fields.Float(required=True, validate=lambda n: n >= 0 and n <= 100)


@api.route('/api/disciplines/packet_corruption')
class PacketCorruptionResource(flask_restful.Resource):

    def __init__(self):
        self.tc = Tc.adapter('eth1')

    def get(self):
        corruption = self.tc.disciplines.get('corrupt', NoneAttributes)
        return {'percent': corruption.percent}, 200

    def post(self):

        def _post(data):
            disciplines = self.tc.disciplines
            disciplines['corrupt'] = PacketCorruption(data['percent'])
            self.tc.apply(disciplines)

        return handle_json_request(PacketCorruptionSchema(), _post)


@api.route('/api/disciplines/packet_corruption/clear')
class ClearPacketCorruptionResource(flask_restful.Resource):

    def __init__(self):
        self.tc = Tc.adapter('eth1')

    def post(self):

        def _post(data):
            disciplines = self.tc.disciplines
            if 'corrupt' in disciplines:
                del disciplines['corrupt']
            self.tc.apply(disciplines)

        return handle_json_request(None, _post)
