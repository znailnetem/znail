"""
Emulates a network disconnect by powering down the built in USB hub.

In many ways, this is equivalent of disconnecting the network cable.
"""

import os
import time

import flask_restplus
import marshmallow

from znail.netem.tc import Tc
from znail.netem.usb import Usb
from znail.ui import api
from znail.ui.util import json_request_handler


class DisconnectSchema(marshmallow.Schema):
    disconnect = marshmallow.fields.Boolean(required=True)


_usb = Usb()
disconnect_schema = DisconnectSchema()
disconnect_model = api.model(
    "Disconnect",
    {
        "disconnect": flask_restplus.fields.Boolean(),
    },
)


@api.route("/api/disconnect")
class DisconnectResource(flask_restplus.Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tc = Tc.adapter("eth1")

    @api.response(200, "Success", disconnect_model)
    def get(self, *args, **kwargs):
        return {"disconnect": not _usb.enabled}, 200

    @json_request_handler(disconnect_schema, disconnect_model)
    def post(self, data):
        if data["disconnect"]:
            _usb.disable_all_usb_ports()
        else:
            _usb.enable_all_usb_ports()
            while not self._poll_network_interface("eth1"):
                time.sleep(0.1)
            self.tc.apply(self.tc.disciplines)

    def _poll_network_interface(self, name):
        if os.getenv("ZNAIL_FORCE_INTERFACE_UP", False):
            return True
        return name in os.listdir("/sys/class/net/")


@api.route("/api/disconnect/clear")
class ClearDisconnectResource(flask_restplus.Resource):
    @json_request_handler()
    def post(self, data):
        _usb.enable_all_usb_ports()
