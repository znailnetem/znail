import unittest
from unittest.mock import patch

from znail.netem.ipredirect import IpRedirect, IpRedirectDescriptor
from znail.ui import app


class TestIpRedirect(unittest.TestCase):
    def setUp(self):
        ip_redirect_clear_patcher = patch.object(IpRedirect, "_clear")
        self.ip_redirect_clear = ip_redirect_clear_patcher.start()
        self.addCleanup(ip_redirect_clear_patcher.stop)

        ip_redirect_apply_patcher = patch.object(IpRedirect, "_apply")
        self.ip_redirect_apply = ip_redirect_apply_patcher.start()
        self.addCleanup(ip_redirect_apply_patcher.stop)

        self.client = app.test_client()

    def tearDown(self):
        self.client.post("/api/ipredirect/clear")

    def test_empty(self):
        response = self.client.get("/api/ipredirect")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_can_be_set(self):
        response = self.client.post(
            "/api/ipredirect",
            json=[
                {
                    "ip": "1.2.3.4",
                    "port": 80,
                    "destination_ip": "2.3.4.5",
                    "destination_port": 8080,
                    "protocol": "tcp",
                }
            ],
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "ok"})

        self.ip_redirect_apply.assert_called_once_with(
            {
                IpRedirectDescriptor(
                    ip="1.2.3.4", port=80, destination_ip="2.3.4.5", destination_port=8080, protocol="tcp"
                )
            }
        )

        response = self.client.get("/api/ipredirect")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json,
            [
                {
                    "ip": "1.2.3.4",
                    "port": 80,
                    "destination_ip": "2.3.4.5",
                    "destination_port": 8080,
                    "protocol": "tcp",
                }
            ],
        )

    def test_multiple_entries(self):
        response = self.client.post(
            "/api/ipredirect",
            json=[
                {
                    "ip": "1.2.3.4",
                    "port": 80,
                    "destination_ip": "2.3.4.5",
                    "destination_port": 8080,
                    "protocol": "tcp",
                },
                {
                    "ip": "2.3.4.5",
                    "port": 8080,
                    "destination_ip": "3.4.5.6",
                    "destination_port": 80,
                    "protocol": "udp",
                },
            ],
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "ok"})

        last_call = sorted(self.ip_redirect_apply.call_args[0][0])
        self.assertEqual(
            last_call,
            sorted(
                [
                    IpRedirectDescriptor(
                        ip="1.2.3.4", port=80, destination_ip="2.3.4.5", destination_port=8080, protocol="tcp"
                    ),
                    IpRedirectDescriptor(
                        ip="2.3.4.5", port=8080, destination_ip="3.4.5.6", destination_port=80, protocol="udp"
                    ),
                ]
            ),
        )

        response = self.client.get("/api/ipredirect")
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            {
                "ip": "1.2.3.4",
                "port": 80,
                "destination_ip": "2.3.4.5",
                "destination_port": 8080,
                "protocol": "tcp",
            },
            response.json,
        )
        self.assertIn(
            {
                "ip": "2.3.4.5",
                "port": 8080,
                "destination_ip": "3.4.5.6",
                "destination_port": 80,
                "protocol": "udp",
            },
            response.json,
        )

    def test_can_not_be_set_to_invalid_value(self):
        response = self.client.post("/api/ipredirect", json={"invalid": "data"})
        self.assertEqual(response.status_code, 422)

    def test_bad_request(self):
        response = self.client.post("/api/ipredirect")
        self.assertEqual(response.status_code, 400)

    def test_can_be_cleared(self):
        response = self.client.post("/api/ipredirect/clear")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "ok"})

        self.ip_redirect_clear.assert_called_once_with()
