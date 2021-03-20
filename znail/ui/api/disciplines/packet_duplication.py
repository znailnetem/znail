import flask_restplus
import marshmallow

from znail.netem.disciplines import PacketDuplication
from znail.netem.tc import Tc
from znail.ui import api
from znail.ui.util import NoneAttributes, json_request_handler


class PacketDuplicationSchema(marshmallow.Schema):
    percent = marshmallow.fields.Float(required=True, validate=lambda n: n >= 0 and n <= 100)


packet_duplication_schema = PacketDuplicationSchema()
packet_duplication_model = api.model("PacketDuplication", {"percent": flask_restplus.fields.Float(min=0, max=100)})


@api.route("/api/disciplines/packet_duplication")
class PacketDuplicationResource(flask_restplus.Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tc = Tc.adapter("eth1")

    @api.response(200, "Success", packet_duplication_model)
    def get(self):
        duplication = self.tc.disciplines.get("duplicate", NoneAttributes)
        return {"percent": duplication.percent}, 200

    @json_request_handler(packet_duplication_schema, packet_duplication_model)
    def post(self, data):
        disciplines = self.tc.disciplines
        disciplines["duplicate"] = PacketDuplication(data["percent"])
        self.tc.apply(disciplines)


@api.route("/api/disciplines/packet_duplication/clear")
class ClearPacketDuplicationResource(flask_restplus.Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tc = Tc.adapter("eth1")

    @json_request_handler()
    def post(self, data):
        disciplines = self.tc.disciplines
        if "duplicate" in disciplines:
            del disciplines["duplicate"]
        self.tc.apply(disciplines)
