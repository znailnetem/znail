"""
Emulates a network disconnect by powering down the built in USB hub.

In many ways, this is equivalent of disconnecting the network cable.
"""

import flask_restful
import marshmallow

from znail.netem.usb import Usb
from znail.ui import api
from znail.ui.util import handle_json_request


class DisconnectSchema(marshmallow.Schema):
    disconnect = marshmallow.fields.Boolean(required=True)


_usb = Usb()


@api.route('/api/disconnect')
class DisconnectResource(flask_restful.Resource):

    def get(self):
        return {'disconnected': not _usb.enabled}, 200

    def post(self):

        def _post(data):
            if data['disconnect']:
                _usb.disable_all_usb_ports()
            else:
                _usb.enable_all_usb_ports()

        return handle_json_request(DisconnectSchema(), _post)


@api.route('/api/disconnect/clear')
class ClearDisconnectResource(flask_restful.Resource):

    def post(self):

        def _post(data):
            _usb.enable_all_usb_ports()

        return handle_json_request(None, _post)
