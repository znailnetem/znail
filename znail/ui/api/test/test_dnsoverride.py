import unittest
from unittest.mock import patch

from znail.netem.dnsoverride import DnsOverrideDescriptor, DnsOverrides
from znail.ui import app


class TestDnsOverride(unittest.TestCase):
    def setUp(self):
        dns_overrides_clear_patcher = patch.object(DnsOverrides, "_clear")
        self.dns_overrides_clear = dns_overrides_clear_patcher.start()
        self.addCleanup(dns_overrides_clear_patcher.stop)

        dns_overrides_apply_patcher = patch.object(DnsOverrides, "_apply")
        self.dns_overrides_apply = dns_overrides_apply_patcher.start()
        self.addCleanup(dns_overrides_apply_patcher.stop)

        self.client = app.test_client()

    def tearDown(self):
        self.client.post("/api/dnsoverride/clear")

    def test_empty(self):
        response = self.client.get("/api/dnsoverride")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_can_be_set(self):
        response = self.client.post("/api/dnsoverride", json=[{"hostname": "a.com", "ip_address": "1.2.3.4"}])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "ok"})

        self.dns_overrides_apply.assert_called_once_with(
            {DnsOverrideDescriptor(hostname="a.com", ip_address="1.2.3.4")}
        )

        response = self.client.get("/api/dnsoverride")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [{"hostname": "a.com", "ip_address": "1.2.3.4"}])

    def test_multiple_entries(self):
        response = self.client.post(
            "/api/dnsoverride",
            json=[{"hostname": "a.com", "ip_address": "1.2.3.4"}, {"hostname": "b.com", "ip_address": "2.3.4.5"}],
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "ok"})

        last_call = sorted(self.dns_overrides_apply.call_args[0][0])
        self.assertEqual(
            last_call,
            sorted(
                [
                    DnsOverrideDescriptor(hostname="a.com", ip_address="1.2.3.4"),
                    DnsOverrideDescriptor(hostname="b.com", ip_address="2.3.4.5"),
                ]
            ),
        )

        response = self.client.get("/api/dnsoverride")
        self.assertEqual(response.status_code, 200)
        self.assertIn({"hostname": "a.com", "ip_address": "1.2.3.4"}, response.json)
        self.assertIn({"hostname": "b.com", "ip_address": "2.3.4.5"}, response.json)

    def test_can_be_updated(self):
        response = self.client.post("/api/dnsoverride", json=[{"hostname": "a.com", "ip_address": "1.2.3.4"}])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "ok"})

        self.dns_overrides_apply.assert_called_once_with(
            {DnsOverrideDescriptor(hostname="a.com", ip_address="1.2.3.4")}
        )

        response = self.client.get("/api/dnsoverride")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [{"hostname": "a.com", "ip_address": "1.2.3.4"}])

        response = self.client.post("/api/dnsoverride", json=[{"hostname": "a.com", "ip_address": "2.3.4.5"}])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "ok"})

        self.dns_overrides_apply.assert_called_with({DnsOverrideDescriptor(hostname="a.com", ip_address="2.3.4.5")})

        response = self.client.get("/api/dnsoverride")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [{"hostname": "a.com", "ip_address": "2.3.4.5"}])

    def test_can_not_be_set_to_invalid_value(self):
        response = self.client.post("/api/dnsoverride", json={"invalid": "data"})
        self.assertEqual(response.status_code, 422)

    def test_bad_request(self):
        response = self.client.post("/api/dnsoverride")
        self.assertEqual(response.status_code, 400)

    def test_can_be_cleared(self):
        response = self.client.post("/api/dnsoverride/clear")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "ok"})

        self.dns_overrides_clear.assert_called_once_with()
