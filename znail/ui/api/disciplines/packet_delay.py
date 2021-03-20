import flask_restplus
import marshmallow

from znail.netem.disciplines import PacketDelay
from znail.netem.tc import Tc
from znail.ui import api
from znail.ui.util import NoneAttributes, json_request_handler


class PacketDelaySchema(marshmallow.Schema):
    milliseconds = marshmallow.fields.Integer(required=True, validate=lambda n: n > 0)


packet_delay_schema = PacketDelaySchema()
packet_delay_model = api.model("PacketDelay", {"milliseconds": flask_restplus.fields.Integer()})


@api.route("/api/disciplines/packet_delay")
class PacketDelayResource(flask_restplus.Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tc = Tc.adapter("eth1")

    @api.response(200, "Success", packet_delay_model)
    def get(self):
        delay = self.tc.disciplines.get("delay", NoneAttributes)
        return {"milliseconds": delay.milliseconds}, 200

    @json_request_handler(packet_delay_schema, packet_delay_model)
    def post(self, data):
        disciplines = self.tc.disciplines
        disciplines["delay"] = PacketDelay(data["milliseconds"])
        self.tc.apply(disciplines)


@api.route("/api/disciplines/packet_delay/clear")
class ClearPacketDelayResource(flask_restplus.Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tc = Tc.adapter("eth1")

    @json_request_handler()
    def post(self, data):
        disciplines = self.tc.disciplines
        if "delay" in disciplines:
            del disciplines["delay"]
        self.tc.apply(disciplines)
