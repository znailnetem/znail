import unittest
from unittest.mock import ANY, patch

from znail.netem.tc import Tc
from znail.netem.usb import Usb
from znail.ui import app
from znail.ui.api.disconnect import DisconnectResource


class TestDisconnect(unittest.TestCase):
    def setUp(self):
        disable_usb_ports_patcher = patch.object(Usb, "_disable_usb_ports")
        self.disable_usb_ports = disable_usb_ports_patcher.start()
        self.addCleanup(disable_usb_ports_patcher.stop)

        enable_usb_ports_patcher = patch.object(Usb, "_enable_usb_ports")
        self.enable_usb_ports = enable_usb_ports_patcher.start()
        self.addCleanup(enable_usb_ports_patcher.stop)

        tc_clear_patcher = patch.object(Tc, "clear")
        self.tc_clear = tc_clear_patcher.start()
        self.addCleanup(tc_clear_patcher.stop)

        tc_apply_patcher = patch.object(Tc, "apply")
        self.tc_apply = tc_apply_patcher.start()
        self.addCleanup(tc_apply_patcher.stop)

        poll_network_interface_patcher = patch.object(DisconnectResource, "_poll_network_interface")
        self.poll_network_interface = poll_network_interface_patcher.start()
        self.addCleanup(poll_network_interface_patcher.stop)

        self.client = app.test_client()

    def tearDown(self):
        self.client.post("/api/disconnect/clear")

    def test_empty(self):
        response = self.client.get("/api/disconnect")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"disconnect": False})

    def test_can_be_set(self):
        response = self.client.post("/api/disconnect", json={"disconnect": True})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "ok"})

        self.disable_usb_ports.assert_called_once_with()

        response = self.client.get("/api/disconnect")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"disconnect": True})

    def test_can_be_updated(self):
        response = self.client.post("/api/disconnect", json={"disconnect": True})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "ok"})

        self.disable_usb_ports.assert_called_once_with()

        response = self.client.get("/api/disconnect")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"disconnect": True})

        response = self.client.post("/api/disconnect", json={"disconnect": False})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "ok"})

        self.enable_usb_ports.assert_called_once_with()

        response = self.client.get("/api/disconnect")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"disconnect": False})

    def test_can_not_be_set_to_invalid_value(self):
        response = self.client.post("/api/disconnect", json={"invalid": "data"})
        self.assertEqual(response.status_code, 422)

    def test_bad_request(self):
        response = self.client.post("/api/disconnect")
        self.assertEqual(response.status_code, 400)

    def test_can_be_cleared(self):
        response = self.client.post("/api/disconnect/clear")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "ok"})

        self.enable_usb_ports.assert_called_once_with()

    def test_queueing_disciplines_are_reapplied_on_reconnect(self):
        self.client.post("/api/disconnect", json={"disconnect": True})
        self.client.post("/api/disconnect", json={"disconnect": False})

        self.tc_apply.assert_called_once_with(ANY)
