import flask_restplus
import marshmallow

from znail.netem.disciplines import PacketCorruption
from znail.netem.tc import Tc
from znail.ui import api
from znail.ui.util import NoneAttributes, json_request_handler


class PacketCorruptionSchema(marshmallow.Schema):
    percent = marshmallow.fields.Float(required=True, validate=lambda n: n >= 0 and n <= 100)


packet_corruption_schema = PacketCorruptionSchema()
packet_corruption_model = api.model("PacketCorruption", {"percent": flask_restplus.fields.Float(min=0, max=100)})


@api.route("/api/disciplines/packet_corruption")
class PacketCorruptionResource(flask_restplus.Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tc = Tc.adapter("eth1")

    @api.response(200, "Success", packet_corruption_model)
    def get(self):
        corruption = self.tc.disciplines.get("corrupt", NoneAttributes)
        return {"percent": corruption.percent}, 200

    @json_request_handler(packet_corruption_schema, packet_corruption_model)
    def post(self, data):
        disciplines = self.tc.disciplines
        disciplines["corrupt"] = PacketCorruption(data["percent"])
        self.tc.apply(disciplines)


@api.route("/api/disciplines/packet_corruption/clear")
class ClearPacketCorruptionResource(flask_restplus.Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tc = Tc.adapter("eth1")

    @json_request_handler()
    def post(self, data):
        disciplines = self.tc.disciplines
        if "corrupt" in disciplines:
            del disciplines["corrupt"]
        self.tc.apply(disciplines)
