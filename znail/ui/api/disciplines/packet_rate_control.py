import flask_restplus
import marshmallow

from znail.netem.disciplines import RateControl
from znail.netem.tc import Tc
from znail.ui import api
from znail.ui.util import NoneAttributes, json_request_handler


class PacketRateControlSchema(marshmallow.Schema):
    kbit = marshmallow.fields.Integer(required=True, validate=lambda n: n > 0)
    latency_milliseconds = marshmallow.fields.Integer(required=True, validate=lambda n: n > 0)
    burst_bytes = marshmallow.fields.Integer(required=True, validate=lambda n: n > 0)


pakcet_rate_control_schema = PacketRateControlSchema()
packet_rate_control_model = api.model(
    "PacketRateControl",
    {
        "kbit": flask_restplus.fields.Integer(min=0),
        "latency_milliseconds": flask_restplus.fields.Integer(min=0),
        "burst_bytes": flask_restplus.fields.Integer(min=0),
    },
)


@api.route("/api/disciplines/packet_rate_control")
class PacketRateControlResource(flask_restplus.Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tc = Tc.adapter("eth1")

    @api.response(200, "Success", packet_rate_control_model)
    def get(self):
        rate_control = self.tc.disciplines.get("rate", NoneAttributes)
        return {
            "kbit": rate_control.kbit,
            "latency_milliseconds": rate_control.latency_milliseconds,
            "burst_bytes": rate_control.burst_bytes,
        }, 200

    @json_request_handler(pakcet_rate_control_schema, packet_rate_control_model)
    def post(self, data):
        disciplines = self.tc.disciplines
        disciplines["rate"] = RateControl(data["kbit"], data["latency_milliseconds"], data["burst_bytes"])
        self.tc.apply(disciplines)


@api.route("/api/disciplines/packet_rate_control/clear")
class ClearPacketRateControlResource(flask_restplus.Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tc = Tc.adapter("eth1")

    @json_request_handler()
    def post(self, data):
        disciplines = self.tc.disciplines
        if "rate" in disciplines:
            del disciplines["rate"]
        self.tc.apply(disciplines)
