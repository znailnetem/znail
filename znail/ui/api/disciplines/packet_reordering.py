import flask_restplus
import marshmallow

from znail.netem.disciplines import PacketReordering
from znail.netem.tc import Tc
from znail.ui import api
from znail.ui.util import NoneAttributes, json_request_handler


class PacketReorderingSchema(marshmallow.Schema):
    milliseconds = marshmallow.fields.Integer(required=True, validate=lambda n: n > 0)
    percent = marshmallow.fields.Float(required=True, validate=lambda n: n >= 0 and n <= 100)


packet_reordering_schema = PacketReorderingSchema()
packet_reordering_model = api.model(
    "PacketReordering",
    {
        "milliseconds": flask_restplus.fields.Integer(min=0),
        "percent": flask_restplus.fields.Float(min=0, max=100),
    },
)


@api.route("/api/disciplines/packet_reordering")
class PacketReorderingResource(flask_restplus.Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tc = Tc.adapter("eth1")

    @api.response(200, "Success", packet_reordering_model)
    def get(self):
        reordering = self.tc.disciplines.get("reorder", NoneAttributes)
        return {
            "milliseconds": reordering.milliseconds,
            "percent": reordering.percent,
        }, 200

    @json_request_handler(packet_reordering_schema, packet_reordering_model)
    def post(self, data):
        disciplines = self.tc.disciplines
        disciplines["reorder"] = PacketReordering(data["percent"], data["milliseconds"])
        self.tc.apply(disciplines)


@api.route("/api/disciplines/packet_reordering/clear")
class ClearPacketReorderingResource(flask_restplus.Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tc = Tc.adapter("eth1")

    @json_request_handler()
    def post(self, data):
        disciplines = self.tc.disciplines
        if "reorder" in disciplines:
            del disciplines["reorder"]
        self.tc.apply(disciplines)
