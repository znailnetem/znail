import flask_restplus
import marshmallow

from znail.netem.disciplines import PacketLoss
from znail.netem.tc import Tc
from znail.ui import api
from znail.ui.util import NoneAttributes, json_request_handler


class PacketLossSchema(marshmallow.Schema):
    percent = marshmallow.fields.Float(required=True, validate=lambda n: n >= 0 and n <= 100)


packet_loss_schema = PacketLossSchema()
packet_loss_model = api.model("PacketLoss", {"percent": flask_restplus.fields.Float(min=0, max=100)})


@api.route("/api/disciplines/packet_loss")
class PacketLossResource(flask_restplus.Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tc = Tc.adapter("eth1")

    @api.response(200, "Success", packet_loss_model)
    def get(self):
        loss = self.tc.disciplines.get("loss", NoneAttributes)
        return {"percent": loss.percent}, 200

    @json_request_handler(packet_loss_schema, packet_loss_model)
    def post(self, data):
        disciplines = self.tc.disciplines
        disciplines["loss"] = PacketLoss(data["percent"])
        self.tc.apply(disciplines)


@api.route("/api/disciplines/packet_loss/clear")
class ClearPacketLossResource(flask_restplus.Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tc = Tc.adapter("eth1")

    @json_request_handler()
    def post(self, data):
        disciplines = self.tc.disciplines
        if "loss" in disciplines:
            del disciplines["loss"]
        self.tc.apply(disciplines)
