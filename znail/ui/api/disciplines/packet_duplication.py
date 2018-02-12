import flask_restful
import marshmallow

from znail.netem.disciplines import PacketDuplication
from znail.netem.tc import Tc
from znail.ui import api
from znail.ui.util import NoneAttributes, handle_json_request


class PacketDuplicationSchema(marshmallow.Schema):
    percent = marshmallow.fields.Float(required=True, validate=lambda n: n >= 0 and n <= 100)


@api.route('/api/disciplines/packet_duplication')
class PacketDuplicationResource(flask_restful.Resource):

    def __init__(self):
        self.tc = Tc.adapter('eth1')

    def get(self):
        duplication = self.tc.disciplines.get('duplicate', NoneAttributes)
        return {'percent': duplication.percent}, 200

    def post(self):

        def _post(data):
            disciplines = self.tc.disciplines
            disciplines['duplicate'] = PacketDuplication(data['percent'])
            self.tc.apply(disciplines)

        return handle_json_request(PacketDuplicationSchema(), _post)


@api.route('/api/disciplines/packet_duplication/clear')
class ClearPacketDuplicationResource(flask_restful.Resource):

    def __init__(self):
        self.tc = Tc.adapter('eth1')

    def post(self):

        def _post(data):
            disciplines = self.tc.disciplines
            if 'duplicate' in disciplines:
                del disciplines['duplicate']
            self.tc.apply(disciplines)

        return handle_json_request(None, _post)
