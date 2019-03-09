import flask_restplus
import marshmallow

from znail.netem.disciplines import PacketReordering
from znail.netem.tc import Tc
from znail.ui import api
from znail.ui.util import NoneAttributes, handle_json_request


class PacketReorderingSchema(marshmallow.Schema):
    milliseconds = marshmallow.fields.Integer(required=True, validate=lambda n: n > 0)
    percent = marshmallow.fields.Float(required=True, validate=lambda n: n >= 0 and n <= 100)


@api.route('/api/disciplines/packet_reordering')
class PacketReorderingResource(flask_restplus.Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tc = Tc.adapter('eth1')

    def get(self):
        reordering = self.tc.disciplines.get('reorder', NoneAttributes)
        return {
            'milliseconds': reordering.milliseconds,
            'percent': reordering.percent,
        }, 200

    def post(self):

        def _post(data):
            disciplines = self.tc.disciplines
            disciplines['reorder'] = PacketReordering(data['percent'], data['milliseconds'])
            self.tc.apply(disciplines)

        return handle_json_request(PacketReorderingSchema(), _post)


@api.route('/api/disciplines/packet_reordering/clear')
class ClearPacketReorderingResource(flask_restplus.Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tc = Tc.adapter('eth1')

    def post(self):

        def _post(data):
            disciplines = self.tc.disciplines
            if 'reorder' in disciplines:
                del disciplines['reorder']
            self.tc.apply(disciplines)

        return handle_json_request(None, _post)
